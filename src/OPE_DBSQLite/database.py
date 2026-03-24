import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.abspath("dbs")
os.makedirs(BASE_DIR, exist_ok=True)

ENGINES = {}
SESSIONS = {}

Base = declarative_base()

def get_engine(code: str):
    """Return (cached) SQLAlchemy engine for given 3-letter code."""
    code = code.upper()
    db_path = os.path.join(BASE_DIR, f"{code}.db")
    db_url = f"sqlite:///{db_path}"

    if code not in ENGINES:
        engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            future=True
        )
        ENGINES[code] = engine
        SESSIONS[code] = sessionmaker(bind=engine, autoflush=False, autocommit=False)

        # Create required tables on new DB
        Base.metadata.create_all(bind=engine)

    return ENGINES[code], SESSIONS[code]


def get_db(code: str):
    """Session generator for FastAPI dependencies."""
    _, SessionLocal = get_engine(code)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
