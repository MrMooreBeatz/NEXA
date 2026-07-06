from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
while PROJECT_ROOT.name != "moore-awareness" and PROJECT_ROOT.parent != PROJECT_ROOT:
    PROJECT_ROOT = PROJECT_ROOT.parent

MOORE_DIR = PROJECT_ROOT
UPLOAD_DIR = PROJECT_ROOT / "uploads"
MEMORY_DIR = PROJECT_ROOT / "07-operations" / "memory"
CHROMA_DIR = MEMORY_DIR / "chroma"

for p in [UPLOAD_DIR, MEMORY_DIR, CHROMA_DIR]:
    p.mkdir(parents=True, exist_ok=True)
