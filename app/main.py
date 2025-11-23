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
    username = username.strip()

    if not username:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Por favor, escribe un nombre."
        })


    if not username[0].isupper():
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Acceso Denegado: El nombre debe comenzar con una letra Mayúscula."
        })

    user_key = username.lower()

    if user_key in FAKE_USERS_DB:
        user_data = FAKE_USERS_DB[user_key]
        is_auror = (user_data["role"] == "AUROR")
        service = get_spell_service()
        current_spells = service.list_all_spells()

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": user_key,
            "is_auror": is_auror,
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
    user_data = FAKE_USERS_DB.get(user_id)

    if not user_data or user_data["role"] != "AUROR":
        # Recargamos la página pero con un mensaje de error y SIN crear el hechizo
        current_spells = service.list_all_spells()
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": user_id,
            "is_auror": False,  # vista restringida
            "spells": current_spells,
            "error": "ALERTA DE SEGURIDAD: No tienes rango de AUROR para registrar hechizos."
        })

    spell_data = SpellCreate(
        name=name,
        power_level=power_level,
        incantation=incantation,
        description=description
    )

    service.create_spell(spell_data)

    current_spells = service.list_all_spells()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user_id,
        "is_auror": True,
        "spells": current_spells,
        "success": "Hechizo registrado correctamente en el Departamento de Misterios."
    })


@app.get("/spell_detail/{spell_id}", response_class=HTMLResponse)
async def view_spell_detail(
        request: Request,
        spell_id: str,
        service: SpellService = Depends(get_spell_service)
):
    # Buscamos el hechizo en el servicio
    spell = service.get_spell_by_id(spell_id)

    if not spell:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Hechizo no encontrado"})

    return templates.TemplateResponse("spell_detail.html", {"request": request, "spell": spell})