from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vaga import Vaga
from app.models.empresa import Empresa
from app.schemas.vaga import VagaCreate, VagaResponse


router = APIRouter(
    prefix="/api/vagas",
    tags=["Vagas"]
)


@router.post("/", response_model=VagaResponse)
def criar_vaga(
    dados: VagaCreate,
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.id == dados.empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    vaga = Vaga(
        empresa_id=dados.empresa_id,
        titulo=dados.titulo,
        descricao=dados.descricao,
        localizacao=dados.localizacao,
        tecnologias=dados.tecnologias,
        tipo=dados.tipo,
        link=dados.link,
        data_publicacao=dados.data_publicacao
    )

    db.add(vaga)
    db.commit()
    db.refresh(vaga)

    return vaga


@router.get("/", response_model=list[VagaResponse])
def listar_vagas(
    db: Session = Depends(get_db)
):
    return db.query(Vaga).all()


@router.get("/{vaga_id}", response_model=VagaResponse)
def buscar_vaga(
    vaga_id: int,
    db: Session = Depends(get_db)
):
    vaga = db.query(Vaga).filter(
        Vaga.id == vaga_id
    ).first()

    if not vaga:
        raise HTTPException(
            status_code=404,
            detail="Vaga não encontrada"
        )

    return vaga


@router.delete("/{vaga_id}")
def eliminar_vaga(
    vaga_id: int,
    db: Session = Depends(get_db)
):
    vaga = db.query(Vaga).filter(
        Vaga.id == vaga_id
    ).first()

    if not vaga:
        raise HTTPException(
            status_code=404,
            detail="Vaga não encontrada"
        )

    db.delete(vaga)
    db.commit()

    return {
        "mensagem": "Vaga eliminada com sucesso"
    }
    
#Parte Final das Rotas de Vagas para editar e apagar vagas
@router.put("/{vaga_id}", response_model=VagaResponse)
def atualizar_vaga(
    vaga_id: int,
    dados: VagaCreate,
    db: Session = Depends(get_db)
):
    vaga = db.query(Vaga).filter(
        Vaga.id == vaga_id
    ).first()

    if not vaga:
        raise HTTPException(
            status_code=404,
            detail="Vaga não encontrada"
        )

    # Verificar se a empresa existe
    empresa = db.query(Empresa).filter(
        Empresa.id == dados.empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    vaga.empresa_id = dados.empresa_id
    vaga.titulo = dados.titulo
    vaga.descricao = dados.descricao
    vaga.localizacao = dados.localizacao
    vaga.tecnologias = dados.tecnologias
    vaga.tipo = dados.tipo
    vaga.link = dados.link
    vaga.data_publicacao = dados.data_publicacao

    db.commit()
    db.refresh(vaga)

    return vaga
    
