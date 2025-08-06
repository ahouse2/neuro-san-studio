import base64
import queue
import time
from datetime import datetime
from io import BytesIO

from flask import Blueprint, jsonify, request

from apps.legal_discovery.database import db
from apps.legal_discovery.models import MessageAuditLog
from coded_tools.legal_discovery import RetrievalChatAgent
from coded_tools.legal_discovery.timeline_builder import TimelineManager
from .extensions import socketio


# Blueprint for chat routes and Socket.IO events
# Exposed under /chat/*
chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

user_input_queue = queue.Queue()
thread_started = False


def background_thread():
    while True:
        try:
            user_input = user_input_queue.get(timeout=0.1)
            if user_input == "exit":
                break
        except queue.Empty:
            time.sleep(0.1)


@socketio.on("connect", namespace="/chat")
def on_connect():
    global thread_started  # pylint: disable=global-statement
    if not thread_started:
        socketio.start_background_task(background_thread)
        thread_started = True


@socketio.on("user_input", namespace="/chat")
def handle_user_input(message):
    user_input = message.get("data", "")
    if user_input:
        user_input_queue.put(user_input)


def synthesize_voice(text: str, model: str) -> str:
    """Generate base64-encoded audio from text."""
    try:
        from gtts import gTTS

        audio_io = BytesIO()
        gTTS(text=text, lang=model).write_to_fp(audio_io)
        audio_io.seek(0)
        return base64.b64encode(audio_io.read()).decode("utf-8")
    except Exception:  # pragma: no cover - best effort
        return ""


@chat_bp.route("/query", methods=["POST"])
def query_agent():
    data = request.get_json() or {}
    text = data.get("text")
    if not text:
        return jsonify({"status": "error", "error": "text required"}), 400
    tm = TimelineManager()
    case_id = data.get("case_id", 1)
    if text.lower().startswith("timeline summary"):
        return jsonify({"status": "ok", "summary": tm.summarize(case_id)})
    event = tm.upsert_event_from_text(text, case_id)
    if event:
        socketio.emit(
            "update_speech",
            {"data": f"Recorded event on {event['date']}"},
            namespace="/chat",
        )
    user_input_queue.put(text)
    agent = RetrievalChatAgent()
    result = agent.query(
        question=text,
        sender_id=data.get("sender_id", 0),
        conversation_id=data.get("conversation_id"),
    )
    if result.get("facts"):
        socketio.emit(
            "update_speech",
            {"data": "\n".join(result["facts"])},
            namespace="/chat",
        )
        db.session.add(
            MessageAuditLog(
                message_id=result["message_id"],
                sender="assistant",
                transcript="\n".join(result["facts"]),
                voice_model=data.get("voice_model"),
            )
        )
    db.session.add(
        MessageAuditLog(
            message_id=result["message_id"],
            sender="user",
            transcript=text,
            voice_model=data.get("voice_model"),
        )
    )
    db.session.commit()
    return jsonify({"status": "ok", "message_id": result["message_id"]})


@chat_bp.route("/voice", methods=["POST"])
def voice_query():
    data = request.get_json() or {}
    transcript = data.get("transcript")
    if not transcript:
        return jsonify({"status": "error", "error": "transcript required"}), 400
    user_input_queue.put(transcript)
    agent = RetrievalChatAgent()
    result = agent.query(
        question=transcript,
        sender_id=data.get("sender_id", 0),
        conversation_id=data.get("conversation_id"),
    )
    response_text = "\n".join(result.get("facts", []))
    if response_text:
        socketio.emit("update_speech", {"data": response_text}, namespace="/chat")
        audio = synthesize_voice(response_text, data.get("voice_model", "en-US"))
        socketio.emit("voice_output", {"audio": audio}, namespace="/chat")
        db.session.add(
            MessageAuditLog(
                message_id=result["message_id"],
                sender="assistant",
                transcript=response_text,
                voice_model=data.get("voice_model"),
            )
        )
    db.session.add(
        MessageAuditLog(
            message_id=result["message_id"],
            sender="user",
            transcript=transcript,
            voice_model=data.get("voice_model"),
        )
    )
    db.session.commit()
    return jsonify({"status": "ok", "message_id": result["message_id"]})
