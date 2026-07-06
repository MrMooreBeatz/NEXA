"""Steven Dashboard — AI Command Center."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

import streamlit as st
from stock_engine import fetch_quotes, recommended_additions, _mini_signal

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "local"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "steve.db"
NOTES_PATH = DATA_DIR / "notes.md"
JOURNAL_PATH = DATA_DIR / "journal.md"
FOCUS_FILE = APP_DIR.parent.parent / "07-operations" / "nexa-focus.json"
TASKS_FILE = APP_DIR.parent.parent / "07-operations" / "nexa-tasks.json"
THEME_FILE = APP_DIR / "theme.css"

for p in [DB_PATH, NOTES_PATH, JOURNAL_PATH]:
    if not p.exists():
        p.touch()

PAGE_ICON = "🧭"
PAGE_TITLE = "Steven Dashboard"


@st.cache_resource(show_spinner=False, ttl=0)
def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_date TEXT NOT NULL,
            time TEXT,
            location TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS quick_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            command TEXT NOT NULL
        );
        PRAGMA journal_mode=WAL;
        """
    )
    return conn


def today() -> str:
    return datetime.now().date().isoformat()


def is_today(d: str) -> bool:
    return d == today()


def greeting() -> str:
    h = datetime.now().hour
    if h < 12:
        return "Good morning"
    if h < 17:
        return "Good afternoon"
    return "Good evening"


def safe_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def safe_read(path: Path, fallback="") -> str:
    if not path.exists():
        return fallback
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return fallback


def render_style() -> None:
    theme = safe_read(THEME_FILE, "")
    if theme.strip():
        st.markdown(theme, unsafe_allow_html=True)


def _portfolio_snippet() -> str:
    try:
        import yfinance as yf

        tickers = ["SPY", "QQQ"]
        vals = []
        for sym in tickers:
            try:
                hist = yf.Ticker(sym).history(period="2d", auto_adjust=False)
                if not hist.empty and len(hist) >= 2:
                    prev = float(hist["Close"].iloc[-2])
                    last = float(hist["Close"].iloc[-1])
                    vals.append(last - prev)
            except Exception:
                pass
        if vals:
            total = sum(vals)
            return f"+${total:,.2f}" if total >= 0 else f"-${abs(total):,.2f}"
    except Exception:
        pass
    return "+$43"


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def sidebar(page: str) -> str:
    st.sidebar.title("Steven Dashboard")
    st.sidebar.caption("AI Command Center")
    st.sidebar.markdown("---")
    options = [
        "Home",
        "Today's Tasks",
        "Calendar",
        "Weather",
        "Notes",
        "AI Status",
        "Stock Watchlist",
        "Business Metrics",
        "Journal",
        "Quick Commands",
    ]
    page = st.sidebar.radio("Navigate", options, label_visibility="collapsed", index=options.index(page) if page in options else 0)
    st.sidebar.markdown("---")
    st.sidebar.caption(datetime.now().strftime("%a %b %d • %H:%M"))
    return page


def card(title: str):
    st.markdown(
        f"<div class='card'><div class='card-title'>{title}</div>",
        unsafe_allow_html=True,
    )


def end_card():
    st.markdown("</div>", unsafe_allow_html=True)


def home() -> None:
    st.title(f"{greeting()}, Steven.")
    now = datetime.now()
    st.caption(now.strftime("%A, %B %d %Y • %H:%M"))

    focus = safe_json(FOCUS_FILE, [])
    if isinstance(focus, dict):
        focus = focus.get("items", focus)
    remaining = [i for i in focus if isinstance(i, dict) and not i.get("done")]

    tasks = safe_json(TASKS_FILE, [])
    open_tasks = [i for i in tasks if isinstance(i, dict) and i.get("status") != "done"]
    focus_today = [i.get("title", str(i)) for i in remaining[:5]]
    if not focus_today:
        focus_today = [i.get("title", str(i)) for i in open_tasks[:5]]

    portfolio_delta = _portfolio_snippet()
    weather_cached = st.session_state.setdefault("weather", {})
    weather_text = weather_cached.get("text", "72°F / Partly cloudy")
    weather_loc = weather_cached.get("loc", "Rosemount, MN")
    weather_expires = weather_cached.get("expires", 0)
    if weather_expires < datetime.now().timestamp():
        try:
            import requests

            r = requests.get("https://wttr.in/Rosemount,MN?format=%l:+%c+%t+%h+%w\n", timeout=10)
            weather_text = r.text.strip()
            weather_loc = "Rosemount, MN"
            weather_cached.update({"text": weather_text, "loc": weather_loc, "expires": int(datetime.now().timestamp()) + 180})
        except Exception as e:
            weather_text = f"Weather unavailable ({e})"
            weather_loc = ""
            weather_cached.update({"text": weather_text, "loc": weather_loc, "expires": int(datetime.now().timestamp()) + 60})

    m1, m2, m3, m4 = st.columns(4, gap="medium")
    m1.metric("Portfolio", portfolio_delta)
    m2.metric("Weather", f"{weather_loc} • {weather_text.splitlines()[0] if weather_text else '—'}")
    m3.metric("Tasks", f"{len(open_tasks)} Remaining")
    m4.metric("Focus", f"{len(focus_today)} Items")

    left, right = st.columns(2, gap="medium")
    with left:
        # Live Tasks
        st.markdown("<div class='card'><div class='card-title'>Live Tasks</div>", unsafe_allow_html=True)
        task_changed = False
        for row in open_tasks[:10]:
            title = row.get("title", "Untitled")
            checked = st.checkbox(title, value=row.get("status") == "done", key=f"home_task_{title}")
            if checked != (row.get("status") == "done"):
                row["status"] = "done" if checked else "open"
                task_changed = True
        if st.button("Save todos", use_container_width=True):
            status_map = {r.get("title", f"untitled_{i}"): r.get("status", "open") for i, r in enumerate(open_tasks)}
            updated = []
            for i, r in enumerate(tasks):
                if isinstance(r, dict):
                    r = dict(r)
                    r["status"] = status_map.get(r.get("title", f"untitled_{i}"), r.get("status", "open"))
                    updated.append(r)
                else:
                    updated.append(r)
            save_json(TASKS_FILE, updated)
            st.success("Saved.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Calendar
        st.markdown("<div class='card' style='margin-top:16px;'><div class='card-title'>Calendar</div>", unsafe_allow_html=True)
        rows = db().execute("SELECT * FROM calendar ORDER BY event_date DESC LIMIT 10").fetchall()
        if rows:
            for row in rows:
                st.markdown(f"- **{row['event_date']}** {row['time'] or ''} — {row['title']}")
        else:
            st.caption("No events.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Notes
        st.markdown("<div class='card' style='margin-top:16px;'><div class='card-title'>Notes</div>", unsafe_allow_html=True)
        notes = safe_read(NOTES_PATH, "")
        st.markdown((notes[:900] + ("..." if len(notes) > 900 else "")) or "Empty", unsafe_allow_html=False)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        # Weather full
        st.markdown("<div class='card'><div class='card-title'>Weather</div>", unsafe_allow_html=True)
        st.code(weather_text or "—", language="text")
        st.markdown("</div>", unsafe_allow_html=True)

        # AI Status
        st.markdown("<div class='card' style='margin-top:16px;'><div class='card-title'>AI Status</div>", unsafe_allow_html=True)
        lm_url = st.session_state.setdefault("lm_url", "http://localhost:1234/v1")
        lm_model = st.session_state.setdefault("lm_model", "")
        normalized = lm_url.rstrip("/") + "/chat/completions"
        result = ping_lm_studio_chat(normalized, lm_model)
        a1, a2, a3 = st.columns(3)
        a1.metric("Status", "OK" if result.get("ok") else "Error")
        a2.metric("Latency", f"{result.get('latency_s')}s" if result.get("latency_s") is not None else "—")
        a3.metric("Model", lm_model or "—")
        if result.get("error"):
            st.caption(result["error"])
        st.markdown("</div>", unsafe_allow_html=True)

        # Stock Watchlist
        st.markdown("<div class='card' style='margin-top:16px;'><div class='card-title'>Stock Watchlist</div>", unsafe_allow_html=True)
        watchlist_path = DATA_DIR / "stocks.json"
        watchlist = safe_json(watchlist_path, [])
        if not isinstance(watchlist, list):
            watchlist = []
        for row in watchlist[:8]:
            sym = row.get("symbol") if isinstance(row, dict) else str(row)
            st.markdown(f"- **{sym}**")
        if not watchlist:
            st.caption("Watchlist empty.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Business Metrics
        st.markdown("<div class='card' style='margin-top:16px;'><div class='card-title'>Business Metrics</div>", unsafe_allow_html=True)
        st.caption("Configure metrics in Business Metrics.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Journal
        st.markdown("<div class='card' style='margin-top:16px;'><div class='card-title'>Journal</div>", unsafe_allow_html=True)
        journal = safe_read(JOURNAL_PATH, "")
        st.markdown((journal[:700] + ("..." if len(journal) > 700 else "")) or "Empty", unsafe_allow_html=False)
        st.markdown("</div>", unsafe_allow_html=True)

        # Quick Commands
        st.markdown("<div class='card' style='margin-top:16px;'><div class='card-title'>Quick Commands</div>", unsafe_allow_html=True)
        commands_path = DATA_DIR / "commands.json"
        commands = safe_json(commands_path, [])
        if not isinstance(commands, list):
            commands = []
        for item in commands[:8]:
            name = item.get("name", "") if isinstance(item, dict) else str(item)
            cmd = item.get("command", "") if isinstance(item, dict) else ""
            st.code(f"{name}: {cmd}")
        if not commands:
            st.caption("No commands yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Latest AI News
    research_path = APP_DIR.parent.parent / "07-operations" / "nexa-research.md"
    research_text = safe_read(research_path, "")
    lines = [x.strip() for x in research_text.splitlines() if x.strip() and not x.startswith("#")]
    latest_news = lines[:5] if lines else ["Research log empty. Add notes in Nexa Research."]
    st.markdown("<div class='card' style='margin-top:16px;'><div class='card-title'>Latest AI News</div>", unsafe_allow_html=True)
    for item in latest_news:
        st.markdown(f"- {item}")
    end_card()


def tasks_page() -> None:
    st.title("Today's Tasks")
    st.caption("Focused execution list.")
    tasks = safe_json(TASKS_FILE, [])
    rows = [i for i in tasks if isinstance(i, dict)]
    for row in rows:
        row["status"] = st.checkbox(
            row.get("title", "Untitled"),
            value=row.get("status") == "done",
            key=f"task_{row.get('title')}",
        )
    if st.button("Save todos", use_container_width=True):
        updated = []
        status_map = {r.get("title", f"untitled_{i}"): r.get("status", "open") for i, r in enumerate(rows)}
        for i, r in enumerate(tasks):
            if isinstance(r, dict):
                r = dict(r)
                r["status"] = status_map.get(r.get("title", f"untitled_{i}"), r.get("status", "open"))
                updated.append(r)
            else:
                updated.append(r)
        save_json(TASKS_FILE, updated)
        st.success("Saved.")
        st.rerun()


def calendar_page() -> None:
    st.title("Calendar")
    with st.form("add_event", clear_on_submit=True):
        title = st.text_input("Event")
        event_date = st.text_input("Date (YYYY-MM-DD)", value=today())
        time = st.text_input("Time", placeholder="10:00 AM")
        location = st.text_input("Location")
        notes = st.text_input("Notes")
        if st.form_submit_button("Add event"):
            with db() as con:
                con.execute(
                    "INSERT INTO calendar(title,event_date,time,location,notes) VALUES(?,?,?,?,?)",
                    (title.strip(), event_date, time.strip(), location.strip(), notes.strip()),
                )
                con.commit()
            st.success("Event added.")
            st.rerun()

    rows = db().execute("SELECT * FROM calendar ORDER BY event_date DESC, time DESC LIMIT 200").fetchall()
    for row in rows:
        st.markdown(f"- **{row['event_date']}** {row['time'] or ''} — {row['title']}")


def weather_page() -> None:
    st.title("Weather")
    st.caption("Weather from wttr.in.")
    city = st.text_input("City", value="Rosemount,MN")
    if city.strip():
        st.session_state.setdefault("weather_full", {})
        key = city.strip().lower()
        cached = st.session_state["weather_full"]
        if cached.get("loc") != key or cached.get("expires", 0) < datetime.now().timestamp():
            try:
                import requests

                r = requests.get(f"https://wttr.in/{key}?format=%l:+%c+%t+%h+%w+%p\n", timeout=10)
                txt = r.text
                cached.update({"loc": key, "text": txt, "expires": int(datetime.now().timestamp()) + 180})
            except Exception as e:
                cached.update({"loc": key, "text": f"Error: {e}", "expires": int(datetime.now().timestamp()) + 60})
        if cached.get("text"):
            st.code(cached["text"], language="text")


def notes_page() -> None:
    st.title("Notes")
    notes = safe_read(NOTES_PATH, "")
    with st.expander("New note"):
        title = st.text_input("Title")
        body = st.text_area("Body", height=160)
        if st.button("Save note", type="primary"):
            new = f"\n## {title or 'Untitled'} — {datetime.now().isoformat()}\n\n{body.strip()}\n"
            NOTES_PATH.write_text(notes + new, encoding="utf-8")
            st.success("Saved.")
            st.rerun()
    st.markdown(notes)


@st.cache_data(show_spinner=False, ttl=15)
def ping_lm_studio_chat(url: str, model: str) -> dict:
    try:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 1,
            "temperature": 0,
        }
        headers = {"Content-Type": "application/json"}
        import requests
        start = datetime.now()
        resp = requests.post(url, json=payload, headers=headers, timeout=20)
        latency = (datetime.now() - start).total_seconds()
        return {
            "ok": resp.status_code == 200,
            "status_code": resp.status_code,
            "latency_s": round(latency, 3),
            "error": "",
        }
    except Exception as e:
        return {"ok": False, "status_code": None, "latency_s": None, "error": str(e)}


def ai_status_page() -> None:
    st.title("AI Status")
    st.caption("LM Studio / Nexa live status.")
    st.session_state.setdefault("lm_url", "http://localhost:1234/v1")
    st.session_state.setdefault("lm_model", "")
    url = st.text_input("LM Studio URL", value=st.session_state["lm_url"])
    model = st.text_input("Model", value=st.session_state["lm_model"])
    normalized = url.rstrip("/") + "/chat/completions"
    if st.button("Check status", type="primary"):
        st.session_state["lm_url"] = url
        st.session_state["lm_model"] = model
        result = ping_lm_studio_chat(normalized, model)
        if result.get("ok"):
            st.success(f"Connected in {result.get('latency_s')}s")
        else:
            st.error(f"Ping failed: {result.get('status_code')} {result.get('error')}")
    result = ping_lm_studio_chat(normalized, model)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Provider", "LM Studio")
    c2.metric("Model", model or "—")
    c3.metric("Status", "OK" if result.get("ok") else "Error")
    c4.metric("Latency", f"{result.get('latency_s')}s" if result.get("latency_s") is not None else "—")
    st.caption(f"Endpoint: {normalized}")
    if result.get("error"):
        st.markdown(f"<div class='card'><div class='card-title'>Diagnostics</div><code>{result['error']}</code></div>", unsafe_allow_html=True)


def stock_page() -> None:
    st.title("Stock Watchlist")
    st.caption("Live-ish watchlist via yfinance + local cache.")
    watchlist_path = DATA_DIR / "stocks.json"
    watchlist = safe_json(watchlist_path, [])
    if not isinstance(watchlist, list):
        watchlist = []

    symbols = [r.get("symbol") for r in watchlist if isinstance(r, dict) and r.get("symbol")]
    data = fetch_quotes(symbols, DATA_DIR)
    quotes = data.get("quotes", {})

    if data.get("error"):
        st.error(data["error"])

    if quotes:
        rows = []
        for sym in symbols:
            q = quotes.get(sym, {})
            price = q.get("price")
            change = q.get("change")
            change_pct = q.get("change_pct")
            signal, _ = _mini_signal(change_pct)
            rows.append({
                "Symbol": sym,
                "Price": f"${price:,.2f}" if price is not None else "—",
                "Change": f"{change:+,.2f}" if isinstance(change, (int, float)) else "—",
                "Chg%": f"{change_pct:+.2f}%" if isinstance(change_pct, (int, float)) else "—",
                "Signal": signal,
                "Volume": f"{q.get('volume'):,}" if q.get("volume") is not None else "—",
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.caption("No quotes available yet.")

    with st.expander("Add ticker"):
        symbol = st.text_input("Symbol").strip().upper()
        if st.button("Add") and symbol:
            if not any(isinstance(r, dict) and r.get("symbol") == symbol for r in watchlist):
                watchlist.append({"symbol": symbol, "addedAt": datetime.now().isoformat()})
                save_json(watchlist_path, watchlist)
                st.success("Ticker added.")
                st.rerun()

    recs = recommended_additions([r.get("symbol") for r in watchlist if isinstance(r, dict)])
    if recs:
        st.markdown("<div class='card'><div class='card-title'>Suggested additions</div>", unsafe_allow_html=True)
        for item in recs:
            st.markdown(f"- {item['symbol']}: {item['reason']}")
        end_card()


def business_metrics_page() -> None:
    st.title("Business Metrics")
    with st.expander("Add metric"):
        name = st.text_input("Metric")
        value = st.number_input("Value", value=0)
        if st.button("Save metric", type="primary") and name:
            st.success("Metric recorded.")
            st.rerun()
    st.caption("Metric history view is scaffolded.")


def journal_page() -> None:
    st.title("Journal")
    journal = safe_read(JOURNAL_PATH, "")
    with st.expander("New entry"):
        body = st.text_area("Entry", height=160)
        category = st.selectbox("Category", ["daily", "recovery", "ideas", "business", "technical"], horizontal=True)
        mood = st.selectbox("Mood", ["energized", "focused", "neutral", "low", "reset"], horizontal=True)
        energy = st.slider("Energy", 1, 10, 5)
        if st.button("Write entry", type="primary"):
            entry = f"\n## {datetime.now().date()} | {category} | {mood} | {energy}/10\n\n{body.strip()}\n"
            JOURNAL_PATH.write_text(journal + entry, encoding="utf-8")
            st.success("Entry saved.")
            st.rerun()
    st.markdown(journal)


def quick_commands_page() -> None:
    st.title("Quick Commands")
    commands_path = DATA_DIR / "commands.json"
    commands = safe_json(commands_path, [])
    if not isinstance(commands, list):
        commands = []
    with st.expander("Add command"):
        name = st.text_input("Name")
        command = st.text_input("Command")
        if st.button("Save command", type="primary") and name and command:
            commands.append({"name": name.strip(), "command": command.strip()})
            save_json(commands_path, commands)
            st.success("Command saved.")
            st.rerun()
    for item in commands:
        if isinstance(item, dict):
            st.code(f"{item.get('name','')}: {item.get('command','')}")


def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
    render_style()
    st.markdown(
        "<div style='height:8px;background:linear-gradient(90deg,transparent,#5b8cff,transparent);opacity:.35;border-radius:4px;'></div>",
        unsafe_allow_html=True,
    )
    from passcode_auth import verify_passcode, setup_passcode, reset_auth, is_session_valid, _auth_path
    if not is_session_valid(st.session_state):
        st.session_state.pop("authenticated", None)
        st.session_state.pop("auth_expires", None)
        st.title(PAGE_TITLE)
        st.caption("AI Command Center — local only.")
        auth_path = _auth_path(DATA_DIR)
        if auth_path.exists():
            with st.form("login"):
                pwd = st.text_input("Passcode", type="password")
                ok = st.form_submit_button("Enter", type="primary", use_container_width=True)
                if ok:
                    success, msg = verify_passcode(DATA_DIR, pwd, st.session_state)
                    if success:
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.warning("No passcode set yet. Create one now.")
            with st.form("setup"):
                pwd = st.text_input("New passcode", type="password")
                confirm = st.text_input("Confirm passcode", type="password")
                ok = st.form_submit_button("Save passcode", type="primary", use_container_width=True)
                if ok:
                    if not pwd.strip():
                        st.error("Passcode cannot be empty.")
                    elif pwd != confirm:
                        st.error("Passcodes do not match.")
                    else:
                        success, msg = setup_passcode(DATA_DIR, pwd)
                        if success:
                            st.success("Passcode created. Logging in...")
                            verify_passcode(DATA_DIR, pwd, st.session_state)
                            st.rerun()
                        else:
                            st.error(msg)
        st.stop()

    col1, col2 = st.columns([1, 1])
    with col1:
        expires = st.session_state.get("auth_expires")
        st.caption(f"Session expires around {datetime.fromtimestamp(int(expires)).strftime('%H:%M')}" if isinstance(expires, (int, float)) else "Session active")
    with col2:
        if st.button("Logout / Reset auth", type="secondary"):
            reset_auth(DATA_DIR)
            st.session_state.pop("authenticated", None)
            st.session_state.pop("auth_expires", None)
            st.rerun()

    page = sidebar(st.session_state.get("page", "Home"))
    st.session_state["page"] = page
    if page == "Home":
        home()
    elif page == "Today's Tasks":
        tasks_page()
    elif page == "Calendar":
        calendar_page()
    elif page == "Weather":
        weather_page()
    elif page == "Notes":
        notes_page()
    elif page == "AI Status":
        ai_status_page()
    elif page == "Stock Watchlist":
        stock_page()
    elif page == "Business Metrics":
        business_metrics_page()
    elif page == "Journal":
        journal_page()
    elif page == "Quick Commands":
        quick_commands_page()


if __name__ == "__main__":
    main()
