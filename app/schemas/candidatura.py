from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CandidaturaCreate(BaseModel):
    vaga_id: int
    cv: Optional[str] = None
    carta: Optional[str] = None
    tipo_envio: Optional[str] = None


class CandidaturaResponse(BaseModel):
    id: int
    vaga_id: int
    estado: str
    cv: Optional[str] = None
    carta: Optional[str] = None
    tipo_envio: Optional[str] = None
    data_envio: Optional[datetime] = None
    criado_em: datetime

    class Config:
        from_attributes = True
        
#Vai se acrescentar aqui 
class CandidaturaEstado(BaseModel):
    estado: str