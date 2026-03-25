import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config_loader import get_config

BASE_DIR = os.path.abspath("dbs")
os.makedirs(BASE_DIR, exist_ok=True)

ENGINES = {}
SESSIONS = {}

Base = declarative_base()

def get_engine(code: str):
    config = get_config()
    db_key = config["database_map"][code.upper()]  # e.g. sqlite, postgres_main
    engine_key = f"{db_key}_{code}"

    # Return cached engine/session
    if engine_key in ENGINES:
        return ENGINES[engine_key], SESSIONS[engine_key]

    # ----------------------------------------------------
    # ✅ Case 1: SQLite
    # ----------------------------------------------------
    if db_key == "sqlite":
        base_dir = config["sqlite"]["base_dir"]
        os.makedirs(base_dir, exist_ok=True)

        db_path = os.path.join(base_dir, f"{code}.db")
        engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            future=True
        )

    # ----------------------------------------------------
    # ✅ Case 2: PostgreSQL engine group
    # ----------------------------------------------------
    elif db_key.startswith("postgres"):
        pg_cfg = config[db_key]
        url = (
            f"postgresql+psycopg2://{pg_cfg['user']}:{pg_cfg['password']}"
            f"@{pg_cfg['host']}:{pg_cfg['port']}/{pg_cfg['database']}"
        )
        engine = create_engine(url, future=True, pool_pre_ping=True)

        # ✅ schema = code
        schema = code.lower()
        with engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            conn.commit()

        Base.metadata.schema = schema

    else:
        raise ValueError(f"Unknown backend type: {db_key}")

    # Create session
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    # Create tables
    Base.metadata.create_all(engine)

    # Cache engine
    ENGINES[engine_key] = engine
    SESSIONS[engine_key] = SessionLocal

    return engine, SessionLocal


def get_db(code: str):
    """Session generator for FastAPI dependencies."""
    _, SessionLocal = get_engine(code)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
