import streamlit as st
from pathlib import Path
from datetime import datetime
import hashlib

# ---------------------------
# PAGE CONFIG — MUST BE FIRST
# ---------------------------
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
            st.markdown("### AUTH")
            st.caption("NEXA // MOORE AWARENESS")
            with st.form("auth_form", clear_on_submit=False):
                password = st.text_input("Access code", type="password", label_visibility="visible")
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
# THEME
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&family=Share+Tech+Mono&display=swap');

:root {
  --bg-deep: #020404;
  --bg-surface: #0a1210;
  --bg-card: #08110e;
  --text-primary: #d6e6e0;
  --text-secondary: #b3c9c3;
  --text-tertiary: #6f8a83;
  --matrix-green: #00ff41;
  --matrix-dim: rgba(0, 255, 65, 0.25);
  --matrix-glow: rgba(0, 255, 65, 0.55);
  --irobot-blue: #4ac3ff;
  --irobot-dim: rgba(74, 195, 255, 0.25);
  --font-tech: 'Orbitron', sans-serif;
  --font-body: 'Rajdhani', sans-serif;
  --font-mono: 'Share Tech Mono', monospace;
}

* { box-sizing: border-box; }

html, body {
  background-color: var(--bg-deep) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  margin: 0;
  padding: 0;
}

.block-container { padding-top: 3.5rem !important; }
section[data-testid="stSidebar"] {
  background: #030806 !important;
  border-right: 1px solid #12261f !important;
}

.nexa-card {
  background: var(--bg-card);
  border: 1px solid #123126;
  border-radius: 10px;
  padding: 14px 16px;
  box-shadow: 0 0 14px rgba(0,0,0,0.25) inset;
}
.nexa-label {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 1.5px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  margin-bottom: 8px;
}
.nexa-value { color: var(--text-primary); }
.nexa-accent { color: var(--matrix-green); }
.nexa-blue { color: var(--irobot-blue); }
.progress-track {
  background: #0f241c;
  border-radius: 999px;
  height: 6px;
  margin-top: 10px;
  overflow: hidden;
}
.progress-fill {
  background: var(--matrix-green);
  box-shadow: 0 0 10px var(--matrix-glow);
  height: 100%;
  border-radius: 999px;
}

.hud-corner {
  position: fixed;
  width: 14px;
  height: 14px;
  border-color: var(--matrix-green);
  border-style: solid;
  z-index: 999996;
  pointer-events: none;
}
.hud-top-left { top: 44px; left: 10px; border-width: 2px 0 0 2px; }
.hud-top-right { top: 44px; right: 10px; border-width: 2px 2px 0 0; }
.hud-bottom-left { bottom: 10px; left: 10px; border-width: 0 0 2px 2px; }
.hud-bottom-right { bottom: 10px; right: 10px; border-width: 0 2px 2px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='hud-corner hud-top-left'></div><div class='hud-corner hud-top-right'></div><div class='hud-corner hud-bottom-left'></div><div class='hud-corner hud-bottom-right'></div>", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.markdown("<div style='margin-bottom:0.75rem;'><div style='font-size:1.1rem;font-weight:700;color:#e5e5e5;'>NEXA</div><div style='font-size:0.72rem;color:#555;letter-spacing:0.05em;text-transform:uppercase;margin-top:2px;'>Personal OS</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", [
        "Today",
        "Calendar",
        "Tasks",
        "Notes",
        "Journal",
        "Goals",
        "Metrics",
        "Notifications",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.caption(datetime.now().strftime("%a, %b %d • %H:%M"))

# ---------------------------
# TODAY
# ---------------------------
if page == "Today":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>TODAY</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Focus</div><div class='nexa-value'><span class='nexa-accent'>1</span> thing today.</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Status</div><div class='nexa-value'><span class='nexa-accent'>●</span> Online</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Time</div><div class='nexa-value' id='clock'></div></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='nexa-card'><div class='nexa-label'>Top 3</div><div class='nexa-value'>1. Restart NEXA stack<br/>2. Clean docs<br/>3. Journal</div></div>", unsafe_allow_html=True)

# ---------------------------
# CALENDAR
# ---------------------------
elif page == "Calendar":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>CALENDAR</h1>", unsafe_allow_html=True)
    st.markdown("<div class='nexa-card'><div class='nexa-value'><div class='nexa-accent'>TODAY</div><div style='color:#7f9a93;'>10:00 AM — Moore Awareness Check-in</div><div style='color:#7f9a93;'>06:00 PM — Recovery Meeting</div></div></div>", unsafe_allow_html=True)

# ---------------------------
# TASKS
# ---------------------------
elif page == "Tasks":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>TASKS</h1>", unsafe_allow_html=True)
    for i, task in enumerate(["Finish auth system", "Research vector DBs", "Review roadmap"], 1):
        st.markdown(f"<div style='display:flex;align-items:center;gap:10px;margin:8px 0;'><span style='color:#5c8a7d;'>[ ]</span><span style='color:#d6e6e0;'>{i}. {task}</span></div>", unsafe_allow_html=True)

# ---------------------------
# NOTES
# ---------------------------
elif page == "Notes":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>NOTES</h1>", unsafe_allow_html=True)
    note = st.text_area("Quick note", height=160, placeholder="Type anything you want to save.")
    if st.button("Save note"):
        st.success("Note saved.")

# ---------------------------
# JOURNAL
# ---------------------------
elif page == "Journal":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>JOURNAL</h1>", unsafe_allow_html=True)
    entry = st.text_area("New entry", height=200, placeholder="What are you building today?")
    if st.button("Save entry"):
        st.success("Entry saved.")

# ---------------------------
# GOALS
# ---------------------------
elif page == "Goals":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>GOALS</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Moore Awareness Alpha</div><div class='nexa-value'><span class='nexa-accent'>58%</span></div><div class='progress-track'><div class='progress-fill' style='width:58%'></div></div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>NEXA</div><div class='nexa-value'><span class='nexa-blue'>48%</span></div><div class='progress-track'><div class='progress-fill' style='width:48%;background:#4ac3ff;box-shadow:0 0 10px rgba(74,195,255,0.4);'></div></div></div>", unsafe_allow_html=True)

# ---------------------------
# METRICS
# ---------------------------
elif page == "Metrics":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>METRICS</h1>", unsafe_allow_html=True)
    st.markdown("<div class='nexa-card'><div class='nexa-label'>Overview</div><div class='nexa-value'><span class='nexa-accent'>$128,730.45</span> <span style='color:#7f9a93;float:right;'>+1.80% TODAY</span></div><div style='height:8px'></div><div style='display:flex;justify-content:space-between;'><div><span class='nexa-blue'>AVEX</span> <span class='nexa-accent'>+4.21%</span></div><div><span class='nexa-blue'>NVDA</span> <span class='nexa-accent'>+2.18%</span></div></div></div>", unsafe_allow_html=True)

# ---------------------------
# NOTIFICATIONS
# ---------------------------
elif page == "Notifications":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>NOTIFICATIONS</h1>", unsafe_allow_html=True)
    st.markdown("<div class='nexa-card'><div class='nexa-label'>Alerts</div><div class='nexa-value'><div style='color:#7f9a93;'>System online</div><div style='color:#7f9a93;'>Backup pending</div></div></div>", unsafe_allow_html=True)
