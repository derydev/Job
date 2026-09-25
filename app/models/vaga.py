from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base


class Vaga(Base):
    __tablename__ = "vagas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )

    titulo = Column(
        String(200),
        nullable=False
    )

    descricao = Column(
        Text,
        nullable=True
    )

    localizacao = Column(
        String(150),
        nullable=True
    )

    tecnologias = Column(
        String(500),
        nullable=True
    )

    tipo = Column(
        String(100),
        nullable=True
    )

    link = Column(
        String(500),
        nullable=True
    )

    data_publicacao = Column(
        String(50),
        nullable=True
    )

    estado = Column(
        String(50),
        default="nova"
    )