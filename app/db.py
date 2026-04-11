from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/attr_tree"
DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(DATABASE_URL, future=True)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()