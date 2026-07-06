"""Database abstraction layer supporting SQLite and PostgreSQL."""
import os
from pathlib import Path
from urllib.parse import urlparse

try:
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, Session
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False

Base = declarative_base() if SQLALCHEMY_AVAILABLE else None


def get_database_url() -> str:
    """Get database URL from environment or use default SQLite."""
    return os.getenv("DATABASE_URL", "sqlite:///database/nexa.db")


def get_engine(database_url: str = None):
    """Create SQLAlchemy engine from database URL."""
    if not SQLALCHEMY_AVAILABLE:
        raise RuntimeError("SQLAlchemy not installed. Run: pip install sqlalchemy psycopg2-binary")
    
    url = database_url or get_database_url()
    
    # SQLite needs special handling
    if url.startswith("sqlite"):
        db_path = Path(url.replace("sqlite:///", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)
    
    return create_engine(url, pool_pre_ping=True, pool_recycle=3600)


def get_session(engine) -> Session:
    """Create a new database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


# -------- Database Models --------
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class JournalEntry(Base):
    __tablename__ = "journal"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CalendarEvent(Base):
    __tablename__ = "calendar"
    id = Column(String(255), primary_key=True)
    text = Column(String(255), nullable=False)
    ts = Column(DateTime)
    created_at = Column(DateTime)


class Message(Base):
    __tablename__ = "messages"
    id = Column(String(255), primary_key=True)
    role = Column(String(20), nullable=False)
    text = Column(Text, nullable=False)
    ts = Column(DateTime)
    source = Column(String(50))


class MarketQuote(Base):
    __tablename__ = "market"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), unique=True, nullable=False)
    name = Column(String(100))
    price = Column(String(50))
    change = Column(String(20))
    direction = Column(String(10))
    updated_at = Column(DateTime)


def create_tables(engine):
    """Create all tables if they don't exist."""
    if SQLALCHEMY_AVAILABLE:
        Base.metadata.create_all(bind=engine)


def migrate_json_to_sqlite():
    """Migrate existing JSON files to SQLite database."""
    from datetime import datetime
    import json
    from pathlib import Path
    
    db_path = Path("database/nexa.db")
    if db_path.exists():
        return  # Already migrated
    
    engine = get_engine("sqlite:///database/nexa.db")
    create_tables(engine)
    
    db = get_session(engine)
    try:
        # Helper to read JSON files
        def read_json_file(path):
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except:
                return []
        
        # Migrate tasks
        tasks_data = read_json_file("database/tasks.json")
        for task in tasks_data:
            db_task = Task(
                id=int(task.get("id", 0)),
                text=task.get("text", ""),
                done=task.get("done", False),
                created_at=datetime.fromisoformat(task.get("ts", datetime.now().isoformat())),
                updated_at=datetime.fromisoformat(task.get("ts", datetime.now().isoformat()))
            )
            db.merge(db_task)
        
        # Migrate notes
        notes_data = read_json_file("database/notes.json")
        for note in notes_data:
            db_note = Note(
                id=int(note.get("id", hash(note.get("text", "")))),
                text=note.get("text", ""),
                created_at=datetime.fromisoformat(note.get("ts", datetime.now().isoformat())),
                updated_at=datetime.fromisoformat(note.get("ts", datetime.now().isoformat()))
            )
            db.merge(db_note)
        
        # Migrate journal entries
        journal_data = read_json_file("database/journal.json")
        for entry in journal_data:
            db_entry = JournalEntry(
                id=int(entry.get("id", hash(entry.get("text", "")))),
                text=entry.get("text", ""),
                created_at=datetime.fromisoformat(entry.get("ts", datetime.now().isoformat())),
                updated_at=datetime.fromisoformat(entry.get("ts", datetime.now().isoformat()))
            )
            db.merge(db_entry)
        
        # Migrate calendar events
        calendar_data = read_json_file("database/calendar.json")
        for event in calendar_data:
            db_event = CalendarEvent(
                id=str(event.get("id", hash(event.get("text", "")))),
                text=event.get("text", ""),
                ts=datetime.fromisoformat(event.get("ts", datetime.now().isoformat())),
                created_at=datetime.fromisoformat(event.get("ts", datetime.now().isoformat()))
            )
            db.merge(db_event)
        
        # Migrate messages
        messages_data = read_json_file("database/messages.json")
        for msg in messages_data:
            db_msg = Message(
                id=str(msg.get("id", hash(msg.get("text", "")))),
                role=msg.get("role", "user"),
                text=msg.get("text", ""),
                ts=datetime.fromisoformat(msg.get("ts", datetime.now().isoformat())),
                source=msg.get("source", "unknown")
            )
            db.merge(db_msg)
        
        # Migrate market data
        market_data = read_json_file("database/market.json")
        for quote in market_data:
            db_quote = MarketQuote(
                symbol=quote.get("symbol", ""),
                name=quote.get("name", ""),
                price=quote.get("price", ""),
                change=quote.get("change", ""),
                direction=quote.get("direction", ""),
                updated_at=datetime.now()
            )
            db.merge(db_quote)
        
        db.commit()
        print("✅ Migration completed successfully")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        db.close()


def init_database():
    """Initialize database and run migrations if needed."""
    database_url = get_database_url()
    
    if database_url.startswith("sqlite"):
        # Run JSON to SQLite migration
        migrate_json_to_sqlite()
    
    engine = get_engine(database_url)
    create_tables(engine)
    return engine
