from pydantic import BaseModel
from typing import Optional


class EmpresaCreate(BaseModel):
    nome: str
    email: Optional[str] = None
    website: Optional[str] = None
    localizacao: Optional[str] = None


class EmpresaResponse(BaseModel):
    id: int
    nome: str
    email: Optional[str] = None
    website: Optional[str] = None
    localizacao: Optional[str] = None

    class Config:
        from_attributes = True