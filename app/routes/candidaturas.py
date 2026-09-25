from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.candidatura import Candidatura
from app.models.vaga import Vaga
#Aqui Vou subistituir 
from app.schemas.candidatura import (
    CandidaturaCreate,
    CandidaturaResponse,
    CandidaturaEstado
)


router = APIRouter(
    prefix="/api/candidaturas",
    tags=["Candidaturas"]
)


# =========================
# CRIAR CANDIDATURA
# =========================
@router.post("/", response_model=CandidaturaResponse)
def criar_candidatura(
    dados: CandidaturaCreate,
    db: Session = Depends(get_db)
):
    # Verificar se a vaga existe
    vaga = db.query(Vaga).filter(
        Vaga.id == dados.vaga_id
    ).first()

    if not vaga:
        raise HTTPException(
            status_code=404,
            detail="Vaga não encontrada"
        )

    candidatura = Candidatura(
        vaga_id=dados.vaga_id,
        estado="preparada",
        cv=dados.cv,
        carta=dados.carta,
        tipo_envio=dados.tipo_envio
    )

    db.add(candidatura)
    db.commit()
    db.refresh(candidatura)

    return candidatura


# =========================
# LISTAR CANDIDATURAS
# =========================
@router.get("/", response_model=list[CandidaturaResponse])
def listar_candidaturas(
    db: Session = Depends(get_db)
):
    return db.query(Candidatura).all()


# =========================
# BUSCAR POR ID
# =========================
@router.get("/{candidatura_id}", response_model=CandidaturaResponse)
def buscar_candidatura(
    candidatura_id: int,
    db: Session = Depends(get_db)
):
    candidatura = db.query(Candidatura).filter(
        Candidatura.id == candidatura_id
    ).first()

    if not candidatura:
        raise HTTPException(
            status_code=404,
            detail="Candidatura não encontrada"
        )

    return candidatura

# Vamos acrescentar =========

@router.patch("/{candidatura_id}/estado", response_model=CandidaturaResponse)
def atualizar_estado(
    candidatura_id: int,
    dados: CandidaturaEstado,
    db: Session = Depends(get_db)
):
    candidatura = db.query(Candidatura).filter(
        Candidatura.id == candidatura_id
    ).first()

    if not candidatura:
        raise HTTPException(
            status_code=404,
            detail="Candidatura não encontrada"
        )

    estados_permitidos = [
        "preparada",
        "enviada",
        "em_analise",
        "entrevista",
        "aceite",
        "rejeitada"
    ]

    if dados.estado not in estados_permitidos:
        raise HTTPException(
            status_code=400,
            detail="Estado inválido"
        )

    candidatura.estado = dados.estado

# Se a candidatura foi enviada pela primeira vez,
# guardar automaticamente a data e hora do envio
    if dados.estado == "enviada" and candidatura.data_envio is None:
        candidatura.data_envio = datetime.now()

    db.commit()
    db.refresh(candidatura)

    return candidatura