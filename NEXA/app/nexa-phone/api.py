from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
from datetime import datetime
import json

BASE = Path(__file__).resolve().parent
DB = BASE / "database"
DB.mkdir(parents=True, exist_ok=True)

TASKS_FILE = DB / "tasks.json"
NOTES_FILE = DB / "notes.json"
JOURNAL_FILE = DB / "journal.json"

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []

def write_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

app = Flask(__name__, static_folder=".", static_url_path="")

@app.get("/")
def index():
    return send_from_directory(BASE, "index.html")

@app.get("/api/tasks")
def tasks_get():
    return jsonify(read_json(TASKS_FILE))

@app.post("/api/tasks")
def tasks_post():
    payload = request.get_json(silent=True) or {}
    tasks = read_json(TASKS_FILE)
    if payload.get("action") == "toggle":
        updated = []
        for t in tasks:
            if t.get("id") == payload.get("id"):
                t = {**t, "done": not t.get("done", False)}
            updated.append(t)
        write_json(TASKS_FILE, updated)
        return jsonify(updated)
    if payload.get("action") == "add" and payload.get("text"):
        new_id = max((t.get("id", 0) for t in tasks), default=0) + 1
        tasks.append({"id": new_id, "text": payload["text"], "done": False})
        write_json(TASKS_FILE, tasks)
        return jsonify(tasks)
    if payload.get("action") == "delete":
        write_json(TASKS_FILE, [t for t in tasks if t.get("id") != payload.get("id")])
        return jsonify(read_json(TASKS_FILE))
    return jsonify(tasks)

@app.get("/api/notes")
def notes_get():
    return jsonify(read_json(NOTES_FILE))

@app.post("/api/notes")
def notes_post():
    payload = request.get_json(silent=True) or {}
    notes = read_json(NOTES_FILE)
    if payload.get("text"):
        notes.insert(0, {"text": payload["text"], "ts": datetime.now().isoformat()})
    if payload.get("action") == "clear":
        notes = []
    write_json(NOTES_FILE, notes)
    return jsonify(notes)

@app.get("/api/journal")
def journal_get():
    return jsonify(read_json(JOURNAL_FILE))

@app.post("/api/journal")
def journal_post():
    payload = request.get_json(silent=True) or {}
    entries = read_json(JOURNAL_FILE)
    if payload.get("text"):
        entries.insert(0, {"text": payload["text"], "ts": datetime.now().isoformat()})
    if payload.get("action") == "clear":
        entries = []
    write_json(JOURNAL_FILE, entries)
    return jsonify(entries)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
