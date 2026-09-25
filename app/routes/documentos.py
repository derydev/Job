from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import uuid

from app.database import get_db
from app.models.documento import Documento


router = APIRouter(
    prefix="/api/documentos",
    tags=["Documentos"]
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads" / "cvs"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/cv")
async def upload_cv(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Aceitar apenas PDF
    if arquivo.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Apenas ficheiros PDF são permitidos"
        )

    # Gerar um nome único
    nome_arquivo = f"{uuid.uuid4()}.pdf"

    caminho_fisico = UPLOAD_DIR / nome_arquivo
    caminho_db = f"uploads/cvs/{nome_arquivo}"

    try:
        # 1. Guardar o PDF na pasta
        with caminho_fisico.open("wb") as buffer:
            shutil.copyfileobj(
                arquivo.file,
                buffer
            )

        # 2. Criar registo na base de dados
        documento = Documento(
            nome_original=arquivo.filename,
            arquivo=nome_arquivo,
            tipo="cv",
            caminho=caminho_db
        )

        db.add(documento)
        db.commit()
        db.refresh(documento)

    except Exception as erro:
        db.rollback()

        # Se o ficheiro foi criado mas a BD falhou,
        # removemos o ficheiro para não deixar lixo
        if caminho_fisico.exists():
            caminho_fisico.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao guardar o CV: {str(erro)}"
        )

    finally:
        await arquivo.close()

    return {
        "mensagem": "CV enviado com sucesso",
        "documento_id": documento.id,
        "nome_original": documento.nome_original,
        "arquivo": documento.arquivo,
        "tipo": documento.tipo,
        "caminho": documento.caminho,
        "criado_em": documento.criado_em
    }