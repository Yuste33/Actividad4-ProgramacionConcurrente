from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.spell_schema import SpellCreate, SpellOut
from app.services.spell_service import SpellService
from app.core.security import get_current_user, check_role_auror

router = APIRouter()

spell_service_instance = SpellService()
def get_spell_service():
    return spell_service_instance
@router.post("/", response_model=SpellOut)
def create_new_spell(
        spell_in: SpellCreate,
        service: SpellService = Depends(get_spell_service),
        current_user: str = Depends(check_role_auror)
):
    return service.create_spell(spell_in)

@router.get("/", response_model=List[SpellOut])
def read_spells(
        service: SpellService = Depends(get_spell_service),
        current_user: str = Depends(get_current_user)
):
    return service.list_all_spells()

@router.get("/{spell_id}", response_model=SpellOut)
def read_spell_by_id(
        spell_id: str,
        service: SpellService = Depends(get_spell_service),
        current_user: str = Depends(get_current_user)
):
    spell =service.get_spell_by_id(spell_id)
    if not spell:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El hechizo buscado no existe"
        )
    return spell