import streamlit as st
from pathlib import Path
from datetime import datetime
import hashlib
import json

st.set_page_config(page_title="NEXA", page_icon="◈", layout="wide")

# ---------------------------
# AUTH
# ---------------------------
AUTHORIZED_HASH = "dde64fbb753a23bae83d7a8e279855e62d8cd8c5fc2305748fe6359fb865df28"

def check_auth():
    if st.session_state.get("nexa_authenticated"):
        return True
    with st.container():
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("<div style='text-align:center; margin-bottom:18px;'><h1 style='color:#00d4aa; font-size:1.6rem; margin:0; letter-spacing:0.06em;'>NEXA</h1><p style='color:#6d8a83; font-size:0.72rem; letter-spacing:0.12em; text-transform:uppercase; margin-top:4px;'>Personal OS</p></div>", unsafe_allow_html=True)
            with st.form("auth_form", clear_on_submit=False, border=True):
                password = st.text_input("Access code", type="password", placeholder="••••••••", label_visibility="collapsed")
                submitted = st.form_submit_button("ENTER", use_container_width=True, type="primary")
                if submitted:
                    if password and hashlib.sha256(password.encode()).hexdigest() == AUTHORIZED_HASH:
                        st.session_state["nexa_authenticated"] = True
                        st.session_state["nexa_authenticated_at"] = datetime.now().isoformat()
                        st.rerun()
                    else:
                        st.error("Access denied")
    return False

if not check_auth():
    st.stop()

# ---------------------------
# PHONE THEME
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --bg-deep: #04070a;
  --bg-card: #0b1115;
  --bg-surface: #111a20;
  --text-primary: #e4ecf1;
  --text-secondary: #8ba0ab;
  --text-muted: #3f5a66;
  --accent: #00d4aa;
  --accent-dim: rgba(0, 212, 170, 0.12);
  --accent-strong: rgba(0, 212, 170, 0.28);
  --border: #162028;
  --blue: #4da6ff;
  --red: #ff5f6d;
  --font: 'Inter', system-ui, sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  background: var(--bg-deep) !important;
  color: var(--text-primary) !important;
  font-family: var(--font) !important;
  overflow-x: hidden;
}

.stApp { background: var(--bg-deep) !important; }
.stApp [data-testid*="block"], main, [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"], [data-testid="stForm"] {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.stButton > button {
  background: var(--bg-card) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  font-family: var(--font) !important;
  font-weight: 500 !important;
  transition: all 0.12s ease !important;
}
.stButton > button:hover {
  background: var(--bg-surface) !important;
  border-color: var(--accent-strong) !important;
}
[data-testid="stFormSubmitButton"] > button {
  background: var(--accent) !important;
  color: #000 !important;
  border: none !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
}

.stTextInput input, .stTextArea textarea, input[type="password"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-primary) !important;
  border-radius: 10px !important;
}
.stSuccess { background: var(--accent-dim) !important; color: var(--accent) !important; }

.status-pill {
  display: inline-block;
  padding: 4px 10px;
  background: var(--accent-dim);
  border: 1px solid var(--accent-strong);
  border-radius: 999px;
  color: var(--accent);
  font-size: 0.75rem;
  font-weight: 500;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.35; }
}
.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  background: var(--accent);
  border-radius: 50%;
  margin-right: 6px;
  animation: pulse 3s ease-in-out infinite;
  vertical-align: middle;
}

.divider { height: 1px; background: linear-gradient(to right, transparent, var(--border), transparent); margin: 14px 0; border: none; }

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px 16px;
}
.card-metric {
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--accent);
  margin-top: 4px;
}
.card-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 500;
  margin-bottom: 6px;
}
.card-caption {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 2px;
}

.progress-track {
  height: 5px;
  background: var(--bg-surface);
  border-radius: 999px;
  margin-top: 10px;
  overflow: hidden;
}
.progress-fill {
  background: var(--accent);
  height: 100%;
  border-radius: 999px;
}

.app-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.app-tile {
  display: flex !important;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 6px 12px;
  border-radius: 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.15s ease;
  font-family: var(--font);
}
.app-tile:hover {
  background: var(--bg-surface);
  border-color: var(--accent-strong);
}
.app-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: var(--accent-dim);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: var(--accent);
}
.app-label {
  font-size: 11px;
  color: var(--text-secondary);
  text-align: center;
  font-weight: 500;
}

.bottom-dock {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(8, 12, 15, 0.8);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-top: 1px solid var(--border);
  padding: 10px 0 14px;
  z-index: 999999;
}
.dock-row {
  display: flex !important;
  justify-content: center !important;
  gap: 32px !important;
}
.dock-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}
.dock-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  font-size: 14px;
}
.dock-item.active .dock-icon, .dock-item:hover .dock-icon {
  background: var(--accent-dim);
  border-color: var(--accent-strong);
  color: var(--accent);
}
.dock-label { font-size: 10px; color: var(--text-muted); letter-spacing: 0.04em; }
.dock-item.active .dock-label, .dock-item:hover .dock-label { color: var(--accent); }

.main-area { padding-bottom: 110px; }

.task-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
}
.task-row:last-child { border-bottom: none; }
.task-checkbox {
  width: 18px;
  height: 18px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: transparent;
  font-size: 12px;
  flex-shrink: 0;
}
.task-checkbox.done {
  background: var(--accent);
  border-color: var(--accent);
  color: #000;
}
.task-text { color: var(--text-secondary); font-size: 0.95rem; }
.task-text.done { text-decoration: line-through; color: var(--text-muted); }

.note-card, .journal-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 10px;
}
.note-meta, .journal-meta {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-bottom: 4px;
}
.note-body, .journal-body { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5; }

.cal-day {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px;
  min-height: 80px;
}
.cal-day.today {
  border-color: var(--accent-strong);
}
.cal-day-header {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 6px;
}
.cal-day-number {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}
.cal-day.today .cal-day-number { color: var(--accent); }
.cal-event {
  font-size: 0.75rem;
  color: var(--text-secondary);
  background: var(--bg-surface);
  border-radius: 6px;
  padding: 4px 6px;
  margin-top: 6px;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}
.notification-item:last-child { border-bottom: none; }
.notification-dot {
  width: 6px;
  height: 6px;
  background: var(--accent);
  border-radius: 50%;
  margin-top: 6px;
  flex-shrink: 0;
}
.notification-content { color: var(--text-secondary); font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# DATA STORE
# ---------------------------
DB_DIR = Path(r"C:\Users\Home\moore-awareness\NEXA\database")
DB_DIR.mkdir(parents=True, exist_ok=True)

TASKS_FILE = DB_DIR / "tasks.json"
NOTES_FILE = DB_DIR / "notes.json"
JOURNAL_FILE = DB_DIR / "journal.json"

def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def get_tasks():
    return load_json(TASKS_FILE, [
        {"id": 1, "text": "Finish auth system", "done": False},
        {"id": 2, "text": "Research vector DBs", "done": False},
        {"id": 3, "text": "Review roadmap", "done": False},
    ])

def save_tasks(tasks):
    save_json(TASKS_FILE, tasks)

def get_notes():
    return load_json(NOTES_FILE, [])

def save_notes(notes):
    save_json(NOTES_FILE, notes)

def get_journal():
    return load_json(JOURNAL_FILE, [])

def save_journal(entries):
    save_json(JOURNAL_FILE, entries)

# ---------------------------
# STATE
# ---------------------------
if "phone_screen" not in st.session_state:
    st.session_state.phone_screen = "home"
if "selected_app" not in st.session_state:
    st.session_state.selected_app = None

def go_home():
    st.session_state.phone_screen = "home"
    st.session_state.selected_app = None
    st.rerun()

def open_app(name):
    st.session_state.selected_app = name
    st.session_state.phone_screen = "app"
    st.rerun()

# ---------------------------
# STATUS BAR
# ---------------------------
now = datetime.now()
date_str = now.strftime("%a, %b %d")
st.markdown(f"""
<div style='display:flex; justify-content:space-between; align-items:center; padding:8px 16px; border-bottom:1px solid var(--border);'>
  <span style='color:var(--accent); font-size:13px; font-weight:500;'>{date_str}</span>
  <span style='font-size:13px; font-weight:600; color:var(--text-primary); font-variant-numeric:tabular-nums;' id='nexa-status-clock'>{now.strftime('%H:%M')}</span>
  <span class='status-pill'><span class='status-dot'></span>ONLINE</span>
</div>
<script>
(function tick() {{
  const d = new Date();
  const el = document.getElementById('nexa-status-clock');
  if(el) el.innerHTML = d.toLocaleTimeString('en-US',{{hour:'2-digit', minute:'2-digit'}});
}})();
setInterval(tick, 1000);
</script>
""", unsafe_allow_html=True)

# ---------------------------
# MAIN ROUTER
# ---------------------------
st.markdown("<div class='main-area'></div>", unsafe_allow_html=True)

if st.session_state.phone_screen == "home":
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        st.markdown("<div class='card'><div class='card-label'>Focus</div><div class='card-metric'>1</div><div class='card-caption'>thing today</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'><div class='card-label'>Completed</div><div class='card-metric'>"+str(sum(1 for t in get_tasks() if t.get("done")))+"</div><div class='card-caption'>tasks done</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='card'><div class='card-label'>Streak</div><div class='card-metric'>7</div><div class='card-caption'>days</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='padding:2px 10px; font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.12em; margin-bottom:10px;'>Apps</div>", unsafe_allow_html=True)

    apps = [
        ("Today", "◉"),
        ("Calendar", "⊞"),
        ("Tasks", "✓"),
        ("Notes", "N"),
        ("Journal", "J"),
        ("Goals", "G"),
        ("Metrics", "M"),
        ("Notifications", "!"),
    ]
    for row_start in range(0, len(apps), 4):
        cols = st.columns(4, gap="small")
        for i, (name, icon) in enumerate(apps[row_start:row_start + 4]):
            with cols[i]:
                st.button(label=icon, key=f"app_icon_{name}", use_container_width=True, help=name, on_click=open_app, args=(name,))
                st.markdown(f"<div style='font-size:11px; color:var(--text-secondary); text-align:center; margin-top:4px;'>{name}</div>", unsafe_allow_html=True)

elif st.session_state.phone_screen == "app":
    app_name = st.session_state.selected_app or "App"
    bcol, tcol = st.columns([1, 4], gap="small")
    with bcol:
        st.button("←", key="back_btn", use_container_width=True, on_click=go_home)
    with tcol:
        st.markdown(f"<div style='display:flex; align-items:center; height:100%;'><div style='font-weight:600; font-size:1.1rem; letter-spacing:0.04em;'>{app_name.upper()}</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if app_name == "Today":
        st.markdown("<div class='card'><div class='card-label'>Top 3</div><div style='line-height:1.7; color:var(--text-secondary);'>1. Restart NEXA stack<br/>2. Clean docs<br/>3. Journal</div></div>", unsafe_allow_html=True)

    elif app_name == "Calendar":
        today = datetime.now()
        year = today.year
        month = today.month
        month_name = today.strftime("%B %Y")
        st.markdown(f"<div class='card'><div class='card-label'>{month_name}</div></div>", unsafe_allow_html=True)
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        header_cols = st.columns(7, gap="small")
        for i, day_name in enumerate(days):
            with header_cols[i]:
                st.markdown(f"<div style='text-align:center; font-size:0.75rem; color:var(--text-muted); font-weight:600;'>{day_name}</div>", unsafe_allow_html=True)

        first_day = datetime(year, month, 1).weekday()
        days_in_month = (datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)).day
        blanks = (first_day + 7 - datetime(year, month, 1).weekday()) % 7
        if blanks == 0 and first_day != 0:
            blanks = 7

        calendar_cells = [""] * blanks + list(range(1, days_in_month + 1))
        rows = [calendar_cells[i:i + 7] for i in range(0, len(calendar_cells), 7)]
        for row in rows:
            cols = st.columns(7, gap="small")
            for i, cell in enumerate(row):
                with cols[i]:
                    if cell == "":
                        st.markdown("<div class='cal-day'></div>", unsafe_allow_html=True)
                    else:
                        is_today = cell == today.day
                        events_html = ""
                        if is_today:
                            events_html = "<div class='cal-event'>10:00 AM — Check-in</div><div class='cal-event'>06:00 PM — Recovery Meeting</div>"
                        st.markdown(f"<div class='cal-day {'today' if is_today else ''}'><div class='cal-day-header'>{'Today' if is_today else ''}</div><div class='cal-day-number'>{cell}</div>{events_html}</div>", unsafe_allow_html=True)

    elif app_name == "Tasks":
        tasks = get_tasks()
        for idx, task in enumerate(tasks):
            col1, col2, col3 = st.columns([1, 6, 1], gap="small")
            with col1:
                checkbox_label = "✓" if task.get("done") else ""
                st.button(checkbox_label or " ", key=f"task_done_{task['id']}", use_container_width=True, on_click=lambda t=task: [save_tasks([{**x, 'done': True} if x['id'] == t['id'] else x for x in get_tasks()]), st.rerun()] )

            with col2:
                text_style = "task-text done" if task.get("done") else "task-text"
                st.markdown(f"<div class='{text_style}'>{task['text']}</div>", unsafe_allow_html=True)

            with col3:
                st.button("✕", key=f"task_del_{task['id']}", use_container_width=True, on_click=lambda t=task: [save_tasks([x for x in get_tasks() if x['id'] != t['id']]), st.rerun()] )

        with st.form("new_task_form", clear_on_submit=True, border=True):
            new_task = st.text_input("Add a task", placeholder="Type and press Enter", label_visibility="collapsed")
            if st.form_submit_button("Add", use_container_width=True) and new_task.strip():
                new_id = max([t["id"] for t in get_tasks()] + [0]) + 1
                save_tasks([*get_tasks(), {"id": new_id, "text": new_task.strip(), "done": False}])
                st.rerun()

    elif app_name == "Notes":
        note_text = st.text_area("New note", height=160, placeholder="Type anything you want to save.", label_visibility="collapsed")
        if st.button("Save note", use_container_width=True) and note_text.strip():
            notes = get_notes()
            notes.insert(0, {"id": datetime.now().isoformat(), "text": note_text.strip(), "ts": datetime.now().isoformat()})
            save_notes(notes)
            st.success("Note saved.")
        for note in get_notes()[:10]:
            try:
                dt = datetime.fromisoformat(note["ts"]).strftime("%b %d • %H:%M")
            except Exception:
                dt = note.get("ts", "")
            st.markdown(f"<div class='note-card'><div class='note-meta'>{dt}</div><div class='note-body'>{note['text']}</div></div>", unsafe_allow_html=True)

    elif app_name == "Journal":
        entry = st.text_area("New entry", height=180, placeholder="What are you building today?", label_visibility="collapsed")
        if st.button("Save entry", use_container_width=True) and entry.strip():
            entries = get_journal()
            entries.insert(0, {"id": datetime.now().isoformat(), "text": entry.strip(), "ts": datetime.now().isoformat()})
            save_journal(entries)
            st.success("Entry saved.")
        for e in get_journal()[:10]:
            try:
                dt = datetime.fromisoformat(e["ts"]).strftime("%b %d • %H:%M")
            except Exception:
                dt = e.get("ts", "")
            st.markdown(f"<div class='journal-card'><div class='journal-meta'>{dt}</div><div class='journal-body'>{e['text']}</div></div>", unsafe_allow_html=True)

    elif app_name == "Goals":
        c1, c2 = st.columns(2, gap="small")
        with c1:
            st.markdown("<div class='card'><div class='card-label'>Moore Awareness</div><div class='card-metric'>58%</div><div class='progress-track'><div class='progress-fill' style='width:58%'></div></div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'><div class='card-label'>NEXA</div><div class='card-metric' style='color:var(--blue);'>48%</div><div class='progress-track'><div class='progress-fill' style='width:48%; background:var(--blue);'></div></div></div>", unsafe_allow_html=True)

    elif app_name == "Metrics":
        st.markdown("""
        <div class='card'>
          <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div class='card-label' style='margin:0;'>Portfolio</div>
            <div style='color:var(--accent); font-size:0.8rem; font-weight:500;'>+1.80% TODAY</div>
          </div>
          <div style='font-size:1.6rem; font-weight:600; margin-top:6px; color:var(--accent);'>$128,730.45</div>
          <div style='display:flex; gap:14px; margin-top:12px;'>
            <div><span style='color:var(--blue); font-weight:500;'>AVEX</span> <span style='color:var(--accent); font-size:0.85rem;'>+4.21%</span></div>
            <div><span style='color:var(--blue); font-weight:500;'>NVDA</span> <span style='color:var(--accent); font-size:0.85rem;'>+2.18%</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    elif app_name == "Notifications":
        notifications = [
            "System online",
            "Backup pending",
            "New memory indexed: 3 items",
        ]
        for idx, notification in enumerate(notifications):
            ncol, tcol = st.columns([1, 6], gap="small")
            with ncol:
                st.markdown("<div class='notification-dot'></div>", unsafe_allow_html=True)
            with tcol:
                st.markdown(f"<div class='notification-content'>{notification}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='card'><div class='card-label'>Coming Soon</div><div style='color:var(--text-secondary);'>This section is under development.</div></div>", unsafe_allow_html=True)

else:
    st.button("Home", key="unk_home", on_click=go_home)

# ---------------------------
# BOTTOM DOCK
# ---------------------------
st.markdown(f"""
<div class='bottom-dock'>
  <div class='dock-row'>
    <div class='dock-item {"active" if st.session_state.phone_screen == "home" else ""}'>
      <div class='dock-icon'>◉</div>
      <div class='dock-label'>Home</div>
    </div>
    <div class='dock-item'>
      <div class='dock-icon'>+</div>
      <div class='dock-label'>New</div>
    </div>
    <div class='dock-item'>
      <div class='dock-icon'>★</div>
      <div class='dock-label'>Fav</div>
    </div>
    <div class='dock-item'>
      <div class='dock-icon'>⚙</div>
      <div class='dock-label'>More</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
