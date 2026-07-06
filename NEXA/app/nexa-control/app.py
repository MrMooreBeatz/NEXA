from pathlib import Path
from datetime import datetime
from flask import Flask, session, jsonify, request, send_from_directory
from dotenv import load_dotenv
import os, json, traceback, hashlib

try:
    from flask_compress import Compress
except Exception:  # pragma: no cover - fallback when package unavailable
    class _DummyCompress:
        def __init__(self, app=None):
            if app is not None:
                self.app = app
    Compress = _DummyCompress  # type: ignore[misc,assignment]

BASE = Path(__file__).resolve().parent
APP_PATH = BASE / "app"
APP_PATH.mkdir(parents=True, exist_ok=True)
load_dotenv(BASE / ".env")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["JSON_SORT_KEYS"] = False
app.secret_key = os.getenv("FLASK_SECRET_KEY") or "nexa-control-local-fallback-secret-2026"
app.config["PERMANENT_SESSION_LIFETIME"] = 86400 * 30
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 86400
app.config["COMPRESS_MIN_SIZE"] = 1
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = bool(os.getenv("FLASK_SECURE_COOKIES", ""))
Compress(app)

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()
USE_DB = DATABASE_URL.startswith(("postgresql://", "postgres://", "sqlite://"))
DASHBOARD_PASSWORD = (os.getenv("DASHBOARD_PASSWORD") or "").strip()
if not DASHBOARD_PASSWORD:
    DASHBOARD_PASSWORD = "2185"

_base_auth_hashes = (
    hashlib.sha256(DASHBOARD_PASSWORD.encode("utf-8")).hexdigest(),
)

try:
    if USE_DB:
        from database import get_engine, create_tables
        _db = get_engine(DATABASE_URL)
        create_tables(_db)
    else:
        _db = None
except Exception as _db_err:
    print(f"[WARN] DB init skipped: {_db_err}")
    _db = None
    USE_DB = False

# -------- Data stores (local JSON, reuse existing NEXA DB when present) --------
NEXA_DB = BASE.parent / "database"
NEXA_DB.mkdir(parents=True, exist_ok=True)
TASKS_FILE = NEXA_DB / "tasks.json"
NOTES_FILE = NEXA_DB / "notes.json"
JOURNAL_FILE = NEXA_DB / "journal.json"
MARKET_FILE = NEXA_DB / "market.json"
MESSAGES_FILE = NEXA_DB / "messages.json"
CALENDAR_FILE = NEXA_DB / "calendar.json"
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://127.0.0.1:1234/v1/chat/completions")
LM_MODEL = os.getenv("LM_MODEL", "loaded-model")


def read_json(path, default=None):
    if default is None:
        default = []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


# -------- SQLite persistence --------
import sqlite3

DB_PATH = NEXA_DB / "nexa.db"


def db_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def migrate_json_to_sqlite_if_needed():
    if DB_PATH.exists():
        return
    conn = db_connect()
    try:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS kv (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );"""
        )
        json_tables = {
            "tasks": TASKS_FILE,
            "notes": NOTES_FILE,
            "journal": JOURNAL_FILE,
            "market": MARKET_FILE,
            "messages": MESSAGES_FILE,
            "calendar": CALENDAR_FILE,
        }
        now = datetime.now().isoformat()
        with conn:
            for key, path in json_tables.items():
                data = read_json(path, [])
                conn.execute(
                    "INSERT OR REPLACE INTO kv (key, value, updated_at) VALUES (?, ?, ?)",
                    (key, json.dumps(data, default=str), now),
                )
        conn.commit()
    finally:
        conn.close()


# -------- Database abstraction layer --------
def _db_get_all(table_name):
    if not USE_DB or _db is None:
        return None
    try:
        from sqlalchemy import text
        with _db.connect() as conn:
            rows = conn.execute(text(f"SELECT * FROM {table_name} ORDER BY updated_at DESC")).fetchall()
            return [dict(row._mapping) for row in rows]
    except Exception:
        return None


def _db_add(table_name, record):
    if not USE_DB or _db is None:
        return False
    try:
        from sqlalchemy import text
        now = datetime.now().isoformat()
        record = {**record, "updated_at": now, "created_at": now}
        cols = ", ".join(record.keys())
        placeholders = ", ".join([f":{k}" for k in record.keys()])
        with _db.connect() as conn:
            conn.execute(text(f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"), record)
            conn.commit()
        return True
    except Exception:
        return False


def _db_delete(table_name, key_name, key_value):
    if not USE_DB or _db is None:
        return False
    try:
        from sqlalchemy import text
        with _db.connect() as conn:
            conn.execute(text(f"DELETE FROM {table_name} WHERE {key_name} = :kv"), {"kv": str(key_value)})
            conn.commit()
        return True
    except Exception:
        return False


def _pooled_connect():
    """Prod-only: use a pooled scoped connection when available."""
    if not USE_DB or _db is None:
        return None
    try:
        return _db.connect()
    except Exception:
        return None


# -------- Basic health / status --------
@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "NEXA Control", "time": datetime.now().isoformat()})


@app.get("/api/status")
def status():
    try:
        try:
            tasks = read_json(TASKS_FILE, [])
            notes = read_json(NOTES_FILE, [])
            journal = read_json(JOURNAL_FILE, [])
            market = read_json(MARKET_FILE, [])
            calendar = read_json(CALENDAR_FILE, [])
            messages = read_json(MESSAGES_FILE, [])
            tasks_done = len([t for t in tasks if t.get("done") or (t.get("status") or "").lower() == "done"])
            quotes = len([q for q in market if q.get("symbol")])
        except Exception as e:
            tasks = notes = journal = market = calendar = messages = []
            tasks_done = quotes = 0
            print(f"[WARN] status read failed: {e}")

        db_ok = False
        db_path = str(NEXA_DB / "nexa.db")
        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("SELECT 1")
            db_ok = True
        except Exception:
            db_ok = False

        lm_latency_ms = None
        lm_status = "unavailable"
        lm_model = LM_MODEL
        try:
            t0 = datetime.now().timestamp()
            req = request.Request(
                LM_STUDIO_URL.replace("/v1/chat/completions", "/v1/models"),
                method="GET",
                headers={"Accept": "application/json"},
            )
            with request.urlopen(req, timeout=4) as response:
                body = json.loads(response.read().decode("utf-8"))
            lm_latency_ms = round((datetime.now().timestamp() - t0) * 1000)
            model_ids = [m.get("id") for m in (body.get("data") or []) if isinstance(m, dict)]
            lm_status = "online" if model_ids else "empty"
            if not lm_model and model_ids:
                lm_model = model_ids[0]
        except Exception:
            lm_status = "unavailable"

        auth_ready = "READY" if session.get("authed") else "REQUIRED"
        return jsonify({
            "ok": True,
            "time": datetime.now().isoformat(),
            "mode": "online",
            "service": "NEXA Control",
            "auth_ready": auth_ready,
            "connectivity": "Connected" if lm_status == "online" else "Disconnected",
            "module_status": "Online",
            "counts": {
                "tasks": len(tasks),
                "tasks_done": tasks_done,
                "notes": len(notes),
                "journal": len(journal),
                "quotes": quotes,
                "calendar": len(calendar),
                "messages": len(messages),
            },
            "diagnostics": {
                "lm_studio": {
                    "status": lm_status,
                    "model": lm_model,
                    "latency_ms": lm_latency_ms,
                },
                "database": {
                    "status": "ok" if db_ok else "error",
                    "path": db_path,
                },
            },
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e)}), 500


# -------- Auth --------
_login_attempts = []
_MAX_LOGIN_ATTEMPTS = 50
_LOGIN_WINDOW_SECONDS = 600


def _login_rate_limited(remote_addr):
    now = datetime.now().timestamp()
    _login_attempts[:] = [t for t in _login_attempts if now - t < _LOGIN_WINDOW_SECONDS]
    if len(_login_attempts) >= _MAX_LOGIN_ATTEMPTS:
        return True
    _login_attempts.append(now)
    return False


@app.get("/api/session")
def session_status():
    return jsonify({"authed": bool(session.get("authed"))})


@app.post("/api/login")
def login():
    payload = request.get_json(silent=True) or {}
    if _login_rate_limited(request.remote_addr or "unknown"):
        return jsonify({"ok": False, "error": "rate_limited"}), 429
    password = (payload.get("password") or "")
    try:
        pwd = password.strip() if isinstance(password, str) else ""
    except Exception:
        pwd = password or ""
    import hashlib
    h = hashlib.sha256(pwd.encode("utf-8", errors="ignore")).hexdigest()
    if h not in _base_auth_hashes:
        if pwd == DASHBOARD_PASSWORD:
            session["authed"] = True
            session["authed_at"] = datetime.now().isoformat()
            session.permanent = True
            return jsonify({"ok": True})
        return jsonify({"ok": False}), 401
    session["authed"] = True
    session["authed_at"] = datetime.now().isoformat()
    session.permanent = True
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

    if action == "reorder":
        idx_from = payload.get("from_index")
        idx_to = payload.get("to_index")
        try:
            idx_from = int(idx_from)
            idx_to = int(idx_to)
        except Exception:
            return jsonify(read_json(TASKS_FILE, []))
        if 0 <= idx_from < len(tasks) and 0 <= idx_to < len(tasks):
            item = tasks.pop(idx_from)
            tasks.insert(idx_to, item)
            write_json(TASKS_FILE, tasks)
        return jsonify(read_json(TASKS_FILE, []))

    if action == "add" and payload.get("text"):
        new_id = max((int(t.get("id", 0)) for t in tasks), default=0) + 1
        text = (payload.get("text") or "").strip()
        task_type = (payload.get("type") or "idea").strip().lower()
        if task_type not in {"idea", "task", "note"}:
            task_type = "idea"
        tag = (payload.get("tag") or "").strip()
        tasks.append({
            "id": new_id,
            "text": text,
            "done": False,
            "type": task_type,
            "tag": tag or None,
            "created_at": datetime.now().isoformat(),
        })
        write_json(TASKS_FILE, tasks)
        _db_add("tasks", {
            "id": new_id,
            "text": text,
            "done": 0,
            "type": task_type,
            "tag": tag,
            "created_at": datetime.now().isoformat(),
        })
        return jsonify(tasks)

    if action == "update":
        target = payload.get("id")
        task = next((t for t in tasks if str(t.get("id")) == str(target)), None)
        if not task:
            return jsonify(read_json(TASKS_FILE, []))
        if "text" in payload and payload.get("text") is not None:
            task["text"] = payload["text"]
        if "type" in payload:
            task_type = (payload["type"] or "").strip().lower()
            task["type"] = task_type if task_type in {"idea", "task", "note"} else task.get("type", "idea")
        if "tag" in payload:
            task["tag"] = (payload["tag"] or "").strip() or None
        if "done" in payload:
            task["done"] = bool(payload["done"])
        write_json(TASKS_FILE, tasks)
        return jsonify(read_json(TASKS_FILE, []))

    if action == "delete":
        target = payload.get("id")
        write_json(TASKS_FILE, [t for t in tasks if str(t.get("id")) != str(target)])
        _db_delete("tasks", "id", target)
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


# -------- Calendar --------
@app.get("/api/calendar")
def calendar_get():
    return jsonify(read_json(CALENDAR_FILE, []))


@app.post("/api/calendar")
def calendar_post():
    payload = request.get_json(silent=True) or {}
    events = read_json(CALENDAR_FILE, [])
    action = (payload.get("action") or "").lower()
    if action == "add" and payload.get("text"):
        events.append(
            {
                "id": datetime.now().isoformat(),
                "text": payload["text"],
                "ts": datetime.now().isoformat(),
            }
        )
        write_json(CALENDAR_FILE, events)
        return jsonify(events)
    if action == "delete":
        target = payload.get("id")
        write_json(CALENDAR_FILE, [e for e in events if str(e.get("id")) != str(target)])
        return jsonify(read_json(CALENDAR_FILE, []))
    return jsonify(events)


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


@app.get("/api/market/reload")
def market_reload_get():
    return market_reload()


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
        req = request.Request(
            LM_STUDIO_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=120) as response:
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
    migrate_json_to_sqlite_if_needed()
    ensure_market_file()


@app.after_request
def cache_headers(response):
    if request.path.startswith("/static/"):
        response.cache_control.max_age = 86400
        response.cache_control.immutable = True
    return response


if __name__ == "__main__":
    bootstrap()
    app.run(host="127.0.0.1", port=8090, debug=True)
