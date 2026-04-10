"""API routes for notes CRUD."""

from flask import request, jsonify
from models import NoteStore

store = NoteStore()


def register_routes(app):
    @app.route("/api/notes", methods=["GET"])
    def list_notes():
        return jsonify(store.list_all())

    @app.route("/api/notes", methods=["POST"])
    def create_note():
        data = request.get_json()
        note = store.create(data["title"], data.get("body", ""))
        return jsonify(note), 201

    @app.route("/api/notes/<note_id>", methods=["GET"])
    def get_note(note_id):
        note = store.get(note_id)
        if not note:
            return jsonify({"error": "not found"}), 404
        return jsonify(note)

    @app.route("/api/notes/<note_id>", methods=["DELETE"])
    def delete_note(note_id):
        if store.delete(note_id):
            return "", 204
        return jsonify({"error": "not found"}), 404
