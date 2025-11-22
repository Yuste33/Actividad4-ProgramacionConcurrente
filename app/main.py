from fastapi import FastAPI
from app.api.v1.endpoints import spells
from app.core.logging_conf import setup_logging

setup_logging()

app = FastAPI(
    title="Sistema de Gestión Mágica del Ministerio",
    description="Implementación AOP y Modular con FastAPI.",
    version="1.0.0"
)

app.include_router(spells.router, prefix="/api/v1/spells", tags=["Hechizos"])

@app.get("/")
def read_root():
    return {"message": "Sistema Mágico Inicializado. ¡Travesura Realizada!"}