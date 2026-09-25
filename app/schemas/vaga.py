from pydantic import BaseModel
from typing import Optional


class VagaCreate(BaseModel):
    empresa_id: int
    titulo: str
    descricao: Optional[str] = None
    localizacao: Optional[str] = None
    tecnologias: Optional[str] = None
    tipo: Optional[str] = None
    link: Optional[str] = None
    data_publicacao: Optional[str] = None


class VagaResponse(VagaCreate):
    id: int
    estado: Optional[str] = "nova"

    class Config:
        from_attributes = True