"""Exhibit management utilities for the legal discovery module."""

import json
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path

from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

from .database import db
from .models import Document, ExhibitCounter, ExhibitAuditLog


class ExhibitExportError(Exception):
    """Raised when exhibits fail validation prior to export."""


def _get_or_create_counter(case_id: int) -> ExhibitCounter:
    counter = ExhibitCounter.query.filter_by(case_id=case_id).first()
    if counter is None:
        counter = ExhibitCounter(case_id=case_id, next_num=1)
        db.session.add(counter)
        db.session.commit()
    return counter


def get_next_exhibit_counter(case_id: int) -> int:
    counter = _get_or_create_counter(case_id)
    value = counter.next_num
    counter.next_num += 1
    db.session.commit()
    return value


def log_action(case_id: int, document_id: int, action: str, user: str | None = None, details: dict | None = None) -> None:
    log = ExhibitAuditLog(
        case_id=case_id,
        document_id=document_id,
        user=user,
        action=action,
        details=details or {},
    )
    db.session.add(log)
    db.session.commit()


def assign_exhibit_number(document_id: int, title: str | None = None, user: str | None = None) -> str:
    doc = Document.query.get(document_id)
    if doc is None:
        raise ValueError("Document not found")
    next_num = get_next_exhibit_counter(doc.case_id)
    doc.exhibit_number = f"EX_{next_num:04}"
    doc.exhibit_title = title or doc.name
    doc.is_exhibit = True
    db.session.commit()
    log_action(doc.case_id, doc.id, "ASSIGN", user, {"exhibit_number": doc.exhibit_number})
    return doc.exhibit_number


def create_cover_sheet(exhibit: Document) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, f"Exhibit {exhibit.exhibit_number}")
    c.setFont("Helvetica", 14)
    if exhibit.exhibit_title:
        c.drawString(100, 720, exhibit.exhibit_title)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def merge_pdf(cover: BytesIO, exhibit_path: str, writer: PdfWriter) -> None:
    writer.append(PdfReader(cover))
    writer.append(PdfReader(exhibit_path))


def validate_exhibits(case_id: int) -> None:
    exhibits = Document.query.filter_by(case_id=case_id, is_exhibit=True).all()
    for ex in exhibits:
        if not ex.bates_number:
            raise ExhibitExportError(f"Missing Bates number for {ex.exhibit_number}")
        if ex.is_privileged:
            raise ExhibitExportError(f"Exhibit {ex.exhibit_number} is marked privileged")


def generate_binder(case_id: int, output_path: str | None = None) -> str:
    validate_exhibits(case_id)
    exhibits = (
        Document.query.filter_by(case_id=case_id, is_exhibit=True)
        .order_by(Document.exhibit_number)
        .all()
    )
    writer = PdfWriter()
    for exhibit in exhibits:
        cover = create_cover_sheet(exhibit)
        merge_pdf(cover, exhibit.file_path, writer)
    if output_path is None:
        output_path = Path(tempfile.gettempdir()) / f"case_{case_id}_binder.pdf"
    with open(output_path, "wb") as f:
        writer.write(f)
    log_action(case_id, 0, "EXPORT_BINDER", details={"path": str(output_path)})
    return str(output_path)


def export_zip(case_id: int, output_path: str | None = None) -> str:
    validate_exhibits(case_id)
    exhibits = (
        Document.query.filter_by(case_id=case_id, is_exhibit=True)
        .order_by(Document.exhibit_number)
        .all()
    )
    if output_path is None:
        output_path = Path(tempfile.gettempdir()) / f"case_{case_id}_exhibits.zip"
    manifest = []
    with zipfile.ZipFile(output_path, "w") as z:
        for ex in exhibits:
            name = f"{ex.exhibit_number}_{(ex.exhibit_title or '').replace(' ', '_')}.pdf"
            z.write(ex.file_path, name)
            manifest.append(
                {
                    "exhibit_number": ex.exhibit_number,
                    "title": ex.exhibit_title,
                    "path": name,
                    "bates_number": ex.bates_number,
                }
            )
        z.writestr("manifest.json", json.dumps(manifest, indent=2))
    log_action(case_id, 0, "EXPORT_ZIP", details={"path": str(output_path)})
    return str(output_path)

