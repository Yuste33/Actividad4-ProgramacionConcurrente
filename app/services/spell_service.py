import uuid
from typing import Dict
from app.schemas.spell_schema import SpellCreate, SpellOut
from app.core.auditing import audit_log


class Hechizo:
    def __init__(self, name: str, power_level: int, incantation: str, description: str, spell_id: str):
        self.spell_id = spell_id
        self.name = name
        self.power_level = power_level
        self.incantation = incantation
        self.description = description

    def execute(self, user_id: str) -> str:
        # Corrección: Usamos self.description en lugar de self.effect
        if self.power_level > 7:
            return f"¡{self.name} ejecutado por {user_id}! Un hechizo FUERTE. Efecto: {self.description}"
        return f"¡{self.name} ejecutado por {user_id}! Descripcion: {self.description}"


class SpellService:
    def __init__(self):
        self.spells: Dict[str, Hechizo] = {}

    @audit_log
    def create_spell(self, spell_data: SpellCreate) -> Hechizo:
        new_id = str(uuid.uuid4())

        new_spell = Hechizo(
            spell_id=new_id,
            name=spell_data.name,
            power_level=spell_data.power_level,
            incantation=spell_data.incantation,
            description=spell_data.description
        )

        self.spells[new_id] = new_spell
        return new_spell

    def get_spell_by_id(self, spell_id: str) -> Hechizo | None:
        return self.spells.get(spell_id)

    def list_all_spells(self) -> list[Hechizo]:
        return list(self.spells.values())