"""
Camada de CONEXÃO COM O BANCO.
Lê a URL do Postgres da variável de ambiente DATABASE_URL (definida no
docker-compose.yml) e expõe a sessão do SQLAlchemy para o resto da app.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin_estoque:123@localhost:5432/estoque_db"
)

# O Render às vezes entrega a URL como "postgres://", e o SQLAlchemy 2 exige "postgresql://".
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency do FastAPI: abre uma sessão por requisição e sempre fecha."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Cria as tabelas no banco caso ainda não existam (chamado no startup)."""
    Base.metadata.create_all(bind=engine)
