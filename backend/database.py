"""
Configuração do banco de dados SQLite usando SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco SQLite - arquivo app.db será criado na pasta backend
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Configuração do engine SQLite
# check_same_thread=False permite uso em múltiplas threads (necessário para FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Configuração da sessão do banco
# autocommit=False: transações manuais
# autoflush=False: controle manual do flush
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos SQLAlchemy
Base = declarative_base()

def get_db():
    """
    Dependency para obter sessão do banco de dados
    Usado pelo FastAPI para injeção de dependência
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
