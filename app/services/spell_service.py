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
        if self.power_level > 7:
            return f"¡{self.name} ejecutado por {user_id}! Un hechizo de ALTO NIVEL. Efecto: {self.description}"
        return f"¡{self.name} ejecutado por {user_id}! Efecto: {self.description}"


class SpellService:
    def __init__(self):
        self.spells: Dict[str, Hechizo] = {}
        self._populate_initial_data()

    def _populate_initial_data(self):
        initial_spells = [
            ("Wingardium Leviosa", 1, "Wingardium Leviosa", "Hace levitar objetos pequeños."),
            ("Expelliarmus", 4, "Expelliarmus", "Desarma al oponente quitándole su varita."),
            ("Expecto Patronum", 8, "Expecto Patronum",
             "Invoca una encarnación de energía positiva para protegerse de Dementores."),
            ("Avada Kedavra", 10, "Avada Kedavra", "Causa la muerte instantánea. (PROHIBIDO)"),
        ]

        for name, power, incantation, desc in initial_spells:
            new_id = str(uuid.uuid4())
            self.spells[new_id] = Hechizo(name, power, incantation, desc, new_id)

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