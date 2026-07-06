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

/* Streamlit layout tweaks */
.block-container { padding-top: 3.5rem !important; }
section[data-testid="stSidebar"] {
  background: #030806 !important;
  border-right: 1px solid #12261f !important;
}

/* Ticker */
.ticker-strip {
  position: fixed;
  top: 8px;
  left: 8px;
  right: 8px;
  z-index: 999997;
  height: 28px;
  display: flex;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--matrix-green);
  border-radius: 6px;
  box-shadow: 0 0 12px var(--matrix-dim);
  overflow: hidden;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--matrix-green);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}
.ticker-scroll { display: flex; gap: 18px; animation: ticker 28s linear infinite; white-space: nowrap; }
@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-50%); } }

/* Cards */
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

/* HUD corners */
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

/* Navigation pills */
.nav-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 8px;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  border: 1px solid transparent;
}
.nav-pill:hover { background:#0e1f1a; color:#e6f5ee; }
.nav-active {
  background: #0c1d16 !important;
  border-color: #1f4d39 !important;
  color: #d8f7e5 !important;
  box-shadow: 0 0 14px rgba(0,255,65,0.08);
}

/* Floating docs button */
.floating-action {
  position: fixed;
  right: 18px;
  bottom: 18px;
  z-index: 999999;
  background: var(--bg-surface);
  border: 1px solid var(--matrix-green);
  color: var(--matrix-green);
  padding: 8px 12px;
  border-radius: 8px;
  font-family: var(--font-mono);
  font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TICKER
# ---------------------------
st.markdown("""
<div class="ticker-strip">
  <div class="ticker-scroll">
    <span>NYSE</span><span>NASDAQ</span><span>S&amp;P 500</span><span>DOW</span>
    <span>NYSE</span><span>NASDAQ</span><span>S&amp;P 500</span><span>DOW</span>
    <span>NYSE</span><span>NASDAQ</span><span>S&amp;P 500</span><span>DOW</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='hud-corner hud-top-left'></div><div class='hud-corner hud-top-right'></div><div class='hud-corner hud-bottom-left'></div><div class='hud-corner hud-bottom-right'></div>", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.markdown("<div style='margin-bottom:0.75rem;'><div style='font-size:1.1rem;font-weight:700;color:#e5e5e5;'>NEXA</div><div style='font-size:0.72rem;color:#555;letter-spacing:0.05em;text-transform:uppercase;margin-top:2px;'>Moore Awareness</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", ["Home", "AI Chat", "Work", "Memory", "Documents", "Journal", "Portfolio", "Tasks", "Research", "Settings"], label_visibility="collapsed")
    st.markdown("---")
    st.caption(datetime.now().strftime("%a, %b %d • %H:%M"))

# ---------------------------
# HOME
# ---------------------------
if page == "Home":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>COMMAND CENTER</h1>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Mission Progress</div><div class='nexa-value'><span class='nexa-accent'>58%</span> Moore Awareness Alpha</div><div class='progress-track'><div class='progress-fill' style='width:58%'></div></div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Priority</div><div class='nexa-value'><span class='nexa-blue'>Authentication</span><br/><span style='font-size:0.85rem;color:#7f9a93;'>Est. 2 hours</span></div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>System</div><div class='nexa-value'><span class='nexa-accent'>● Online</span><br/>LM Studio connected</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        focus_items = ["Finish auth system", "Research vector DBs", "Review roadmap", "Organize documents", "Daily reflection"]
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Today's Focus</div>", unsafe_allow_html=True)
        for i, item in enumerate(focus_items, 1):
            st.markdown(f"<div style='display:flex;align-items:center;gap:8px;margin:6px 0;'><span style='color:#5c8a7d;'>[{i}]</span><span style='color:#b7d3cb;'>{item}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Ask NEXA</div>", unsafe_allow_html=True)
        prompt = st.text_input("Ask NEXA anything...", label_visibility="collapsed", placeholder="Type a task, question, or note")
        if st.button("Run", use_container_width=True):
            if prompt:
                st.success(f"Logged: {prompt}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Active Projects</div><div class='nexa-value'><div style='display:flex;justify-content:space-between;'><span>Moore Awareness</span><span class='nexa-accent'>72%</span></div><div class='progress-track'><div class='progress-fill' style='width:72%'></div></div><div style='display:flex;justify-content:space-between;margin-top:6px;'><span>NEXA</span><span class='nexa-blue'>48%</span></div><div class='progress-track'><div class='progress-fill' style='width:48%;background:#4ac3ff;box-shadow:0 0 10px rgba(74,195,255,0.4);'></div></div></div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Recent Documents</div><div class='nexa-value'><div style='color:#7f9a93;'>Business Plan.docx <span style='float:right;color:var(--irobot-blue);'>2h</span></div><hr style='border:none;border-top:1px solid #12261f;margin:8px 0;'/><div style='color:#7f9a93;'>Moore Awareness Roadmap.pdf <span style='float:right;color:var(--irobot-blue);'>5h</span></div><hr style='border:none;border-top:1px solid #12261f;margin:8px 0;'/><div style='color:#7f9a93;'>Q2 Financial Overview.xlsx <span style='float:right;color:var(--irobot-blue);'>1d</span></div></div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Calendar</div><div class='nexa-value'><div class='nexa-accent'>TODAY</div><div style='color:#7f9a93;'>10:00 AM — Moore Awareness Check-in</div><div style='color:#7f9a93;'>06:00 PM — Recovery Meeting</div></div></div>", unsafe_allow_html=True)

# ---------------------------
# WORK
# ---------------------------
elif page == "Work":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>WORK</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Active Projects</div><div class='nexa-value'><div style='display:flex;justify-content:space-between;'><span>Moore Awareness</span><span class='nexa-accent'>72%</span></div><div class='progress-track'><div class='progress-fill' style='width:72%'></div></div><div style='display:flex;justify-content:space-between;margin-top:10px;'><span>NEXA</span><span class='nexa-blue'>48%</span></div><div class='progress-track'><div class='progress-fill' style='width:48%;background:#4ac3ff;box-shadow:0 0 10px rgba(74,195,255,0.4);'></div></div><div style='display:flex;justify-content:space-between;margin-top:10px;'><span>So Brrr Water</span><span style='color:#cdb078;'>25%</span></div><div class='progress-track'><div class='progress-fill' style='width:25%;background:#cdb078;box-shadow:0 0 10px rgba(205,176,120,0.4);'></div></div></div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Current Tasks</div><div class='nexa-value'><div style='display:flex;align-items:center;gap:8px;margin:6px 0;'><span style='color:#5c8a7d;'>[ ]</span><span>Finish auth system</span></div><div style='display:flex;align-items:center;gap:8px;margin:6px 0;'><span style='color:#5c8a7d;'>[ ]</span><span>Research vector databases</span></div><div style='display:flex;align-items:center;gap:8px;margin:6px 0;'><span style='color:#5c8a7d;'>[ ]</span><span>Review roadmap</span></div></div></div>", unsafe_allow_html=True)

# ---------------------------
# MEMORY
# ---------------------------
elif page == "Memory":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>MEMORY</h1>", unsafe_allow_html=True)
    st.markdown("<div class='nexa-card'><div class='nexa-label'>Memory Feed</div><div class='nexa-value'><div style='color:#7f9a93;'>New journal entry — 8:15 PM</div><div style='color:#7f9a93;'>Captured 3 new ideas — 6:45 PM</div><div style='color:#7f9a93;'>Document uploaded — 4:30 PM</div></div></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='nexa-card'><div class='nexa-label'>Semantic Search</div>", unsafe_allow_html=True)
    query = st.text_input("Query", label_visibility="collapsed", placeholder="Search memories")
    if st.button("Search"):
        st.info("Search requires embeddings setup.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# DOCUMENTS
# ---------------------------
elif page == "Documents":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>DOCUMENTS</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Upload</div>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Drop files here", type=["pdf","docx","txt","md","csv","json"], accept_multiple_files=True, label_visibility="collapsed")
        if uploaded:
            for f in uploaded:
                st.success(f"Saved: {f.name}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Recent</div><div class='nexa-value'><div style='color:#7f9a93;'>Business Plan.docx</div><div style='color:#7f9a93;'>Moore Awareness Roadmap.pdf</div><div style='color:#7f9a93;'>Q2 Financial Overview.xlsx</div></div></div>", unsafe_allow_html=True)

# ---------------------------
# JOURNAL
# ---------------------------
elif page == "Journal":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>JOURNAL</h1>", unsafe_allow_html=True)
    entry = st.text_area("New entry", height=160, placeholder="What are you building today?")
    if st.button("Save entry"):
        st.success("Entry saved.")

# ---------------------------
# PORTFOLIO
# ---------------------------
elif page == "Portfolio":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>PORTFOLIO</h1>", unsafe_allow_html=True)
    st.markdown("<div class='nexa-card'><div class='nexa-label'>Overview</div><div class='nexa-value'><span class='nexa-accent' style='font-size:1.25rem;'>$128,730.45</span> <span style='color:#7f9a93;float:right;'>+1.80% TODAY</span></div><div style='height:8px'></div><div style='display:flex;justify-content:space-between;'><div><span class='nexa-blue'>AVEX</span> <span class='nexa-accent'>+4.21%</span></div><div><span class='nexa-blue'>NVDA</span> <span class='nexa-accent'>+2.18%</span></div></div></div>", unsafe_allow_html=True)

# ---------------------------
# TASKS
# ---------------------------
elif page == "Tasks":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>TASKS</h1>", unsafe_allow_html=True)
    for i, task in enumerate(["Finish auth system", "Research vector DBs", "Review roadmap"], 1):
        st.markdown(f"<div style='display:flex;align-items:center;gap:10px;margin:8px 0;'><span style='color:#5c8a7d;'>[ ]</span><span style='color:#d6e6e0;'>{i}. {task}</span></div>", unsafe_allow_html=True)

# ---------------------------
# RESEARCH
# ---------------------------
elif page == "Research":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>RESEARCH</h1>", unsafe_allow_html=True)
    st.markdown("<div class='nexa-card'><div class='nexa-label'>Active Thread</div><div class='nexa-value'>Vector databases + embeddings for memory</div></div>", unsafe_allow_html=True)

# ---------------------------
# SETTINGS
# ---------------------------
elif page == "Settings":
    st.markdown("<h1 style='margin-top:0.25rem;font-family:var(--font-tech);font-size:1.4rem;letter-spacing:0.08em;'>SETTINGS</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>LM Studio</div>", unsafe_allow_html=True)
        st.text_input("LM Studio URL", value="http://localhost:1234/v1", key="lm_url")
        st.text_input("Model", value="loaded-model-name", key="lm_model")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='nexa-card'><div class='nexa-label'>Authentication</div>", unsafe_allow_html=True)
        st.success("Authenticated")
        st.caption("Since " + st.session_state.get("nexa_authenticated_at", ""))
        st.markdown("</div>", unsafe_allow_html=True)
