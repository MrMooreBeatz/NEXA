from pathlib import Path
from datetime import datetime
import json

MEMORY_DIR = Path(__file__).resolve().parent.parent / "07-operations" / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
INDEX_FILE = MEMORY_DIR / "index.json"

def _load_index():
    try:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def _save_index(data):
    INDEX_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def add_memory(text, category="general", source="manual"):
    if not text.strip():
        return None
    entry = {
        "text": text.strip(),
        "category": category,
        "source": source,
        "created": datetime.now().isoformat(),
    }
    data = _load_index()
    data.append(entry)
    _save_index(data)
    return entry

def search_memory(query, max_results=5):
    query = query.strip().lower()
    if not query:
        return []
    data = _load_index()
    scored = []
    for item in data:
        text = item.get("text", "").lower()
        score = 0
        if query in text:
            score += 5
        for word in query.split():
            if word and word in text:
                score += 1
        if score:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:max_results]]
