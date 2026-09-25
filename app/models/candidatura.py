from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from app.database import Base


class Candidatura(Base):
    __tablename__ = "candidaturas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vaga_id = Column(
        Integer,
        ForeignKey("vagas.id"),
        nullable=False
    )
    documento_id = Column(
    Integer,
    ForeignKey("documentos.id"),
    nullable=True
)

    estado = Column(
        String(50),
        default="preparada"
    )

    cv = Column(
        String(255),
        nullable=True
    )

    carta = Column(
        Text,
        nullable=True
    )

    tipo_envio = Column(
        String(50),
        nullable=True
    )

    data_envio = Column(
        DateTime,
        nullable=True
    )

    criado_em = Column(
        DateTime,
        default=datetime.now
    )