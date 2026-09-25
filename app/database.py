from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Endereço da nossa base de dados
DATABASE_URL = "sqlite:///./derijobb.db"


# Cria a ligação com a base de dados
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Cria sessões para trabalhar com a base de dados
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base utilizada pelos nossos models
Base = declarative_base()


# Função que fornece uma ligação à base de dados
def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()