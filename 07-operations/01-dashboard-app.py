import streamlit as st
from pathlib import Path
import os

# ---------------------------
# CONFIG
# ---------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS = {
    "Master Roadmap": PROJECT_ROOT / "00-master-roadmap.md",
    "Brand Core": PROJECT_ROOT / "02-brand" / "01-brand-core.md",
    "Content Bank": PROJECT_ROOT / "03-content" / "01-content-idea-bank.md",
    "App Brief": PROJECT_ROOT / "04-app" / "01-app-brief.md",
    "Finance Tracker": PROJECT_ROOT / "05-finance" / "01-finance-tracker.md",
    "Infrastructure": PROJECT_ROOT / "07-operations" / "01-infrastructure-architecture.md",
    "Foundation Blueprint": PROJECT_ROOT / "07-operations" / "02-functional-foundation-blueprint.md",
    "Nexa Context": PROJECT_ROOT / "07-operations" / "nexa-local-context.md",
}

# ---------------------------
# HELPERS
# ---------------------------
@st.cache_data
def load_doc(title, path):
    if not path.exists():
        return f"_File not found: {path}_"
    return path.read_text(encoding="utf-8")

def extract_section(text, heading):
    """Return text after first markdown heading match until next heading or EOF."""
    marker = f"## {heading}"
    idx = text.find(marker)
    if idx == -1:
        return ""
    snippet = text[idx:]
    # cut at next heading of same or higher level
    lines = snippet.splitlines()
    out = []
    for line in lines[1:]:
        if line.startswith("# "):
            break
        out.append(line)
    return "\n".join(out).strip()

def extract_task_lines(text):
    """Find checklist lines in Phase 1 section for quick status."""
    tasks = []
    for raw in text.splitlines():
        if raw.strip().startswith("- [ ]") or raw.strip().startswith("- [x]"):
            tasks.append(raw.strip())
    return tasks

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("Moore Awareness")
st.sidebar.caption("Internal Foundation Dashboard")
page = st.sidebar.radio("Navigate", [
    "Overview",
    "Roadmap Status",
    "Brand",
    "Content",
    "App",
    "Finance",
    "Infrastructure",
    "Nexa Local",
    "Raw Documents",
])

# ---------------------------
# PAGES
# ---------------------------
if page == "Overview":
    st.title("Moore Awareness — System Overview")
    st.subheader("Ecosystem at a glance")

    roadmap = load_doc("Master Roadmap", DOCS["Master Roadmap"])
    brand = load_doc("Brand Core", DOCS["Brand Core"])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Business entity", "MN LLC")
    with c2:
        st.metric("Website", "mooreawareness.com")
    with c3:
        st.metric("Bank", "Think Bank")

    st.markdown("### Active pillars")
    st.markdown(
        "- **Moore Awareness LLC** — umbrella brand\n"
        "- **So Brrr Water + merch** — fastest revenue path\n"
        "- **MSAP** — nonprofit recovery framework, still in development\n"
        "- **So Brrr Streak App** — Free / Moore+ / Orgs\n"
        "- **Nexa** — Steven's personal AI layer on Hermes"
    )

    st.markdown("### Quick status")
    tasks = extract_task_lines(roadmap)
    pending = [t for t in tasks if "- [ ]" in t]
    done = [t for t in tasks if "- [x]" in t]
    st.write(f"Completed foundation items: {len(done)}")
    st.write(f"Open foundation items: {len(pending)}")
    if pending:
        st.markdown("**Currently open:**")
        for t in pending[:8]:
            st.markdown(t.replace("- [ ]", "⬜ ").replace("- [x]", "✅ "))

elif page == "Roadmap Status":
    st.title("Roadmap")
    text = load_doc("Master Roadmap", DOCS["Master Roadmap"])
    st.markdown(text)

elif page == "Brand":
    st.title("Brand Core")
    text = load_doc("Brand Core", DOCS["Brand Core"])
    st.markdown(text)

elif page == "Content":
    st.title("Content Idea Bank")
    text = load_doc("Content Bank", DOCS["Content Bank"])
    st.markdown(text)

elif page == "App":
    st.title("So Brrr Streak App Brief")
    text = load_doc("App Brief", DOCS["App Brief"])
    st.markdown(text)

elif page == "Finance":
    st.title("Finance Tracker")
    text = load_doc("Finance Tracker", DOCS["Finance Tracker"])
    st.markdown(text)

elif page == "Infrastructure":
    st.title("Infrastructure & Architecture")
    text = load_doc("Infrastructure", DOCS["Infrastructure"])
    st.markdown(text)

elif page == "Nexa Local":
    st.title("Nexa Local Context")
    st.caption("This is the file used as system prompt for LM Studio.")
    text = load_doc("Nexa Context", DOCS["Nexa Context"])
    st.markdown(text)

elif page == "Raw Documents":
    st.title("Raw Documents")
    choice = st.selectbox("Choose document", list(DOCS.keys()))
    text = load_doc(choice, DOCS[choice])
    st.markdown(text)
    st.download_button(
        "Download markdown",
        text,
        file_name=DOCS[choice].name,
        mime="text/markdown",
    )

# ---------------------------
# FOOTER
# ---------------------------
st.sidebar.markdown("---")
st.sidebar.write("Foundation built in sessions 1-3.")
st.sidebar.write("Next: launch planning + live data entry.")
