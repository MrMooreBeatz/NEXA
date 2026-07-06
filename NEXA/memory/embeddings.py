from pathlib import Path
from datetime import datetime
import json

PROJECT_ROOT = Path(__file__).resolve().parents[2]
while PROJECT_ROOT.name != "moore-awareness" and PROJECT_ROOT.parent != PROJECT_ROOT:
    PROJECT_ROOT = PROJECT_ROOT.parent

MEMORY_DIR = PROJECT_ROOT / "07-operations" / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
INDEX_FILE = MEMORY_DIR / "index.json"
CHROMA_DIR = MEMORY_DIR / "chroma"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)


def _load_index():
    try:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_index(data):
    INDEX_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def add_memory(text, category="general", source="manual"):
    text = (text or "").strip()
    if not text:
        return None
    entry = {
        "text": text,
        "category": category,
        "source": source,
        "created": datetime.now().isoformat(),
    }
    data = _load_index()
    data.append(entry)
    _save_index(data)
    return entry


def search_memory(query, max_results=5):
    query = (query or "").strip().lower()
    if not query:
        return []
    data = _load_index()
    scored = []
    for item in data:
        body = item.get("text", "").lower()
        score = 0
        if query in body:
            score += 5
        for word in query.split():
            if word and word in body:
                score += 1
        if score:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[: max(1, max_results)]]


def get_chroma_client():
    import chromadb
    from chromadb.config import Settings
    return chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="nexa-memory",
        metadata={"hnsw:space": "cosine"},
    )


def build_embeddings(texts):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(texts, normalize_embeddings=True).tolist()


def seed_default_memories():
    defaults = [
        "Moore Awareness Alpha is in early foundation.",
        "LLC reinstatement and renewal are locked through 12/31/2027.",
        "Dashboard is simplified to core decision-making modules.",
        "Suggested focus today: keep the foundation solid before adding more modules.",
        "Next technical priority: embeddings, ChromaDB, and semantic search.",
    ]
    docs = []
    metas = []
    ids = []
    for i, text in enumerate(defaults):
        docs.append(text)
        metas.append({"source": "seed"})
        ids.append(datetime.now().strftime("%Y%m%d%H%M%S") + f"-seed-{i}")
    if docs:
        collection = get_collection()
        collection.add(documents=docs, embeddings=build_embeddings(docs), metadatas=metas, ids=ids)
        for text in docs:
            add_memory(text, category="seed", source="seed")
    return len(docs)


def semantic_search(query, max_results=5):
    query = (query or "").strip()
    if not query:
        return []
    collection = get_collection()
    q = build_embeddings([query])
    results = collection.query(query_embeddings=q, n_results=max(1, max_results))
    items = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        items.append({"text": doc, "score": 1, "source": meta.get("source", "chroma")})
    return items
