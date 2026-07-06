import json
from pathlib import Path
from datetime import datetime
from flask import Flask, session, jsonify, request, send_from_directory

BASE = Path(__file__).resolve().parent
APP_PATH = BASE / "app"
APP_PATH.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "nexa-control-local-session-key"
BASE_AUTH_HASH = "dde64fbb753a23bae83d7a8e279855e62d8cd8c5fc2305748fe6359fb865df28"
EXTRA_AUTH_HASH = "e73975ed917ecd161b0495eb8d186c8ee93ccc33caf99dbc9e8c4e829a84870d"

# -------- Data stores (local JSON, reuse existing NEXA DB when present) --------
NEXA_DB = BASE.parent / "database"
NEXA_DB.mkdir(parents=True, exist_ok=True)
TASKS_FILE = NEXA_DB / "tasks.json"
NOTES_FILE = NEXA_DB / "notes.json"
JOURNAL_FILE = NEXA_DB / "journal.json"
MARKET_FILE = NEXA_DB / "market.json"
MESSAGES_FILE = NEXA_DB / "messages.json"
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
LM_MODEL = "loaded-model"


def read_json(path, default=None):
    if default is None:
        default = []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


# -------- Basic health / status --------
@app.get("/api/health")
def health():
    now = datetime.now().isoformat()
    return jsonify({"ok": True, "time": now, "service": "nexa-control"})


@app.get("/api/status")
def status():
    tasks = read_json(TASKS_FILE, [])
    notes = read_json(NOTES_FILE, [])
    journal = read_json(JOURNAL_FILE, [])
    market = read_json(MARKET_FILE, [])
    return jsonify(
        {
            "service": "NEXA Control",
            "mode": "online",
            "time": datetime.now().isoformat(),
            "counts": {
                "tasks": len(tasks),
                "notes": len(notes),
                "journal": len(journal),
                "quotes": len(market),
            },
        }
    )


# -------- Auth --------
@app.get("/api/session")
def session_status():
    return jsonify({"authed": bool(session.get("authed"))})


@app.post("/api/login")
def login():
    payload = request.get_json(silent=True) or {}
    password = (payload.get("password") or "").strip()
    import hashlib
    h = hashlib.sha256(password.encode("utf-8", errors="ignore")).hexdigest()
    if h not in (BASE_AUTH_HASH, EXTRA_AUTH_HASH):
        return jsonify({"ok": False}), 401
    session["authed"] = True
    session["authed_at"] = datetime.now().isoformat()
    return jsonify({"ok": True})


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


# -------- Tasks --------
@app.get("/api/tasks")
def tasks_get():
    return jsonify(read_json(TASKS_FILE, []))


@app.post("/api/tasks")
def tasks_post():
    payload = request.get_json(silent=True) or {}
    tasks = read_json(TASKS_FILE, [])
    action = (payload.get("action") or "").lower()
    if action == "toggle":
        target = payload.get("id")
        updated = []
        for t in tasks:
            if str(t.get("id")) == str(target):
                t = {**t, "done": not t.get("done", False)}
            updated.append(t)
        write_json(TASKS_FILE, updated)
        return jsonify(updated)

    if action == "add" and payload.get("text"):
        new_id = max((int(t.get("id", 0)) for t in tasks), default=0) + 1
        tasks.append({"id": new_id, "text": payload.get("text"), "done": False})
        write_json(TASKS_FILE, tasks)
        return jsonify(tasks)

    if action == "delete":
        target = payload.get("id")
        write_json(TASKS_FILE, [t for t in tasks if str(t.get("id")) != str(target)])
        return jsonify(read_json(TASKS_FILE, []))

    return jsonify(tasks)


# -------- Notes --------
@app.get("/api/notes")
def notes_get():
    return jsonify(read_json(NOTES_FILE, []))


@app.post("/api/notes")
def notes_post():
    payload = request.get_json(silent=True) or {}
    notes = read_json(NOTES_FILE, [])
    if payload.get("text"):
        notes.insert(
            0, {"id": datetime.now().isoformat(), "text": payload["text"], "ts": datetime.now().isoformat()}
        )
    if payload.get("action") == "clear":
        notes = []
    write_json(NOTES_FILE, notes)
    return jsonify(notes)


# -------- Journal --------
@app.get("/api/journal")
def journal_get():
    return jsonify(read_json(JOURNAL_FILE, []))


@app.post("/api/journal")
def journal_post():
    payload = request.get_json(silent=True) or {}
    entries = read_json(JOURNAL_FILE, [])
    if payload.get("text"):
        entries.insert(
            0, {"id": datetime.now().isoformat(), "text": payload["text"], "ts": datetime.now().isoformat()}
        )
    if payload.get("action") == "clear":
        entries = []
    write_json(JOURNAL_FILE, entries)
    return jsonify(entries)


# -------- Market default store --------
def ensure_market_file():
    write_json(
        MARKET_FILE,
        [
            {"symbol": "^GSPC", "name": "S&P 500", "price": "5,432.41", "change": "+1.80%", "direction": "up"},
            {"symbol": "^IXIC", "name": "Nasdaq", "price": "17,124.02", "change": "+2.14%", "direction": "up"},
            {"symbol": "^DJI", "name": "Dow", "price": "39,120.86", "change": "-0.34%", "direction": "down"},
            {"symbol": "AVEX", "name": "AVEX", "price": "34.72", "change": "+4.21%", "direction": "up"},
            {"symbol": "NVDA", "name": "NVIDIA", "price": "118.50", "change": "+2.18%", "direction": "up"},
            {"symbol": "AAPL", "name": "Apple", "price": "212.10", "change": "+0.65%", "direction": "up"},
            {"symbol": "TSLA", "name": "Tesla", "price": "177.77", "change": "-1.08%", "direction": "down"},
            {"symbol": "BTC-USD", "name": "Bitcoin", "price": "102,430", "change": "+1.54%", "direction": "up"},
        ],
    )


@app.get("/api/market")
def market_get():
    try:
        return jsonify(read_json(MARKET_FILE, []))
    except Exception:
        ensure_market_file()
        return jsonify(read_json(MARKET_FILE, []))


@app.post("/api/market/reload")
def market_reload():
    ensure_market_file()
    return jsonify(read_json(MARKET_FILE, []))


# -------- Chat / LM Studio --------
@app.get("/api/messages")
def messages_get():
    return jsonify(read_json(MESSAGES_FILE, []))


@app.post("/api/messages")
def messages_post():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify(read_json(MESSAGES_FILE, []))

    messages = read_json(MESSAGES_FILE, [])
    user_msg = {
        "id": datetime.now().isoformat(),
        "role": "user",
        "text": text,
        "ts": datetime.now().isoformat(),
        "source": "operator",
    }
    messages.append(user_msg)

    assistant_text = _lm_reply(messages)
    assistant_msg = {
        "id": datetime.now().isoformat() + "-a",
        "role": "assistant",
        "text": assistant_text,
        "ts": datetime.now().isoformat(),
        "source": "lm-studio",
    }
    messages.append(assistant_msg)
    write_json(MESSAGES_FILE, messages[-200:])
    return jsonify(messages)


def _lm_reply(history):
    try:
        import urllib.request
        import urllib.error

        trimmed = [m for m in history if m.get("text")][-20:]
        payload = {
            "model": LM_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are NEXA, a concise mission-control assistant. "
                        "Use short, direct replies. Avoid filler."
                    ),
                },
                *[{"role": m["role"], "content": m["text"]} for m in trimmed],
            ],
            "temperature": 0.1,
            "max_tokens": 200,
        }
        req = urllib.request.Request(
            LM_STUDIO_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
        choice = (((body.get("choices") or [{}])[0]).get("message") or {})
        return (choice.get("content") or "No response.").strip()
    except Exception:
        return "LM Studio unavailable."


@app.get("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.get("/<path:path>")
def static_proxy(path):
    return send_from_directory(BASE, path)


def bootstrap():
    ensure_market_file()


if __name__ == "__main__":
    bootstrap()
    app.run(host="127.0.0.1", port=8090, debug=True)
