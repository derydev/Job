from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)

    nome_original = Column(
        String(255),
        nullable=False
    )

    arquivo = Column(
        String(255),
        nullable=False,
        unique=True
    )

    tipo = Column(
        String(50),
        default="cv"
    )

    caminho = Column(
        String(500),
        nullable=False
    )

    criado_em = Column(
        DateTime,
        default=datetime.now
    )