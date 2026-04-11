import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config_loader import get_config

# ---------------------------------------------------------
# Base for all models
# ---------------------------------------------------------
Base = declarative_base()

# ---------------------------------------------------------
# Engine & Session caches (per code)
# ---------------------------------------------------------
_ENGINES: dict[str, object] = {}
_SESSIONS: dict[str, sessionmaker] = {}


# ---------------------------------------------------------
# Engine factory (per `code`)
# ---------------------------------------------------------
def get_engine(code: str):
    """
    Returns a (engine, SessionLocal) tuple for a given `code`.

    - Creates engine lazily
    - Creates schema (Postgres) or DB file (SQLite) if missing
    - Automatically creates tables via Base.metadata.create_all()
    """
    code = code.lower()
    config = get_config()

    print("Loaded database_map:", config["database_map"])
    print("Requested code:", code.upper())

    db_key = config["database_map"][code.upper()]
    cache_key = f"{db_key}:{code}"

    # ✅ Return cached engine/session if already created
    if cache_key in _ENGINES:
        return _ENGINES[cache_key], _SESSIONS[cache_key]

    # -----------------------------------------------------
    # SQLite backend
    # -----------------------------------------------------
    if db_key == "sqlite":
        base_dir = config["sqlite"]["base_dir"]
        os.makedirs(base_dir, exist_ok=True)

        db_path = os.path.join(base_dir, f"{code}.db")

        engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            future=True,
        )

    # -----------------------------------------------------
    # PostgreSQL backend (with per-code schema)
    # -----------------------------------------------------
    elif db_key.startswith("postgres"):
        pg_cfg = config[db_key]

        url = (
            f"postgresql+psycopg2://{pg_cfg['user']}:{pg_cfg['password']}"
            f"@{pg_cfg['host']}:{pg_cfg['port']}/{pg_cfg['database']}"
        )

        engine = create_engine(
            url,
            future=True,
            pool_pre_ping=True,
        )

        # ✅ Create schema per code
        schema = code
        with engine.connect() as conn:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
            conn.commit()

        # ✅ Ensure all tables use this schema
        Base.metadata.schema = schema

    else:
        raise ValueError(f"Unknown database backend: {db_key}")

    # -----------------------------------------------------
    # Create session factory
    # -----------------------------------------------------
    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        future=True,
    )

    # -----------------------------------------------------
    # ✅ Automatically create tables (THIS IS KEY)
    # -----------------------------------------------------
    Base.metadata.create_all(bind=engine)

    # -----------------------------------------------------
    # Cache and return
    # -----------------------------------------------------
    _ENGINES[cache_key] = engine
    _SESSIONS[cache_key] = SessionLocal

    return engine, SessionLocal


# ---------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------
def get_db(code: str):
    """
    FastAPI dependency.
    Provides a DB session for a given `code`.
    """
    _, SessionLocal = get_engine(code)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()