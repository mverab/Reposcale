import sys
sys.path.insert(0, "src")

from app import create_app


def test_create_and_list_notes():
    app = create_app()
    client = app.test_client()

    resp = client.post("/api/notes", json={"title": "Test", "body": "Hello"})
    assert resp.status_code == 201

    resp = client.get("/api/notes")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 1


def test_delete_note():
    app = create_app()
    client = app.test_client()

    resp = client.post("/api/notes", json={"title": "Delete me"})
    note_id = resp.get_json()["id"]

    resp = client.delete(f"/api/notes/{note_id}")
    assert resp.status_code == 204
