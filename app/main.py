from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.api.v1.endpoints import spells
from app.core.logging_conf import setup_logging
from app.core.security import FAKE_USERS_DB
from app.schemas.spell_schema import SpellCreate
from app.services.spell_service import SpellService
from app.api.v1.endpoints.spells import get_spell_service

setup_logging()

app = FastAPI(title="Sistema de Gestión Mágica")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(spells.router, prefix="/api/v1/spells", tags=["Hechizos"])


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Renderiza el Login
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...)):

    # La primera letra debe estar en mayusculas
    if not username[0].isupper():
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Acceso Denegado: El nombre debe comenzar con una letra Mayúscula por respeto al protocolo mágico."
        })

    user_key = username.lower()

    if user_key in FAKE_USERS_DB:
        service = get_spell_service()
        current_spells = service.list_all_spells()

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": user_key,
            "spells": current_spells
        })
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Error: Este mago no consta en los archivos del Ministerio."
        })

@app.post("/create_spell_web", response_class=HTMLResponse)
async def create_spell_web(
        request: Request,
        user_id: str = Form(...),
        name: str = Form(...),
        power_level: int = Form(...),
        incantation: str = Form(...),
        description: str = Form(...),
        service: SpellService = Depends(get_spell_service)
):

    spell_data = SpellCreate(
        name=name,
        power_level=power_level,
        incantation=incantation,
        description=description
    )

    # se llama al seervicio
    service.create_spell(spell_data)

    # se carga nuevamente el dashboard
    current_spells = service.list_all_spells()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user_id,
        "spells": current_spells
    })