"""Quick launch check for Steven Dashboard local data/schema."""
from steven_dashboard import get_connection, DATA_DIR
from pathlib import Path

print("data dir:", DATA_DIR)
print("db exists:", (DATA_DIR / "steve.db").exists())
conn = get_connection()
print("has tasks:", conn.execute("SELECT name FROM sqlite_master WHERE name='tasks'").fetchone()["name"])
print("has calendar:", conn.execute("SELECT name FROM sqlite_master WHERE name='calendar'").fetchone()["name"])
