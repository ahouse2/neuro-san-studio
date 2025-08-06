import os
import pytest

os.environ["DATABASE_URL"] = "sqlite://"

from apps.legal_discovery.interface_flask import app, db


@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app.test_client()


def test_theories_suggest(client, monkeypatch):
    monkeypatch.setattr(
        "apps.legal_discovery.theories_routes.LegalTheoryEngine.suggest_theories",
        lambda self: [],
    )
    resp = client.get("/theories/suggest")
    assert resp.status_code == 200
    assert resp.json["theories"] == []


def test_binder_pretrial_export(client, monkeypatch):
    monkeypatch.setattr(
        "apps.legal_discovery.binder_routes.PretrialGenerator.export",
        lambda self, case_id, path: None,
    )
    resp = client.post("/binder/pretrial/export", json={"case_id": 1})
    assert resp.status_code == 200
    assert "path" in resp.json
