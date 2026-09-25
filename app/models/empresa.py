from sqlalchemy import Column, Integer, String
from app.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=True
    )

    website = Column(
        String(255),
        nullable=True
    )

    localizacao = Column(
        String(150),
        nullable=True
    )