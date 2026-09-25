from fastapi import FastAPI

from app.database import Base, engine
from app.models import Empresa, Vaga, Candidatura, Documento
from app.routes.empresas import router as empresas_router
from app.routes.vagas import router as vagas_router
from app.routes.candidaturas import router as candidaturas_router
from app.routes.documentos import router as documentos_router



# Cria as tabelas na base de dados caso ainda não existam
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="DeriJobb API",
    description="API do sistema de procura e gestão de candidaturas",
    version="1.0.0"
)


# Rotas
app.include_router(empresas_router)
app.include_router(vagas_router)
app.include_router(candidaturas_router)
app.include_router(documentos_router)

@app.get("/")
def home():
    return {
        "sistema": "DeriJobb",
        "status": "online"
    }


@app.get("/api/status")
def status():
    return {
        "api": "online",
        "database": "configurada",
        "version": "1.0.0"
    }