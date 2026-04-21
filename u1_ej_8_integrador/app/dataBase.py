import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/fastapi_tp")

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    """Inyección de dependencia para sesiones de DB."""
    with Session(engine) as session:
        yield session