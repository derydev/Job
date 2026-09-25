from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaResponse


router = APIRouter(
    prefix="/api/empresas",
    tags=["Empresas"]
)


@router.post("/", response_model=EmpresaResponse)
def criar_empresa(
    dados: EmpresaCreate,
    db: Session = Depends(get_db)
):

    empresa = Empresa(
        nome=dados.nome,
        email=dados.email,
        website=dados.website,
        localizacao=dados.localizacao
    )

    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return empresa


@router.get("/", response_model=list[EmpresaResponse])
def listar_empresas(
    db: Session = Depends(get_db)
):

    empresas = db.query(Empresa).all()

    return empresas

#Parte dos Delete
from fastapi import HTTPException


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def buscar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    return empresa


@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa(
    empresa_id: int,
    dados: EmpresaCreate,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    empresa.nome = dados.nome
    empresa.email = dados.email
    empresa.website = dados.website
    empresa.localizacao = dados.localizacao

    db.commit()
    db.refresh(empresa)

    return empresa


@router.delete("/{empresa_id}")
def eliminar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    db.delete(empresa)
    db.commit()

    return {
        "mensagem": "Empresa eliminada com sucesso"
    }