from pydantic import BaseModel, Field


class SpellCreate(BaseModel):
    name: str = Field(..., description="Nombre del hechizo")
    power_level: int = Field(...,gt=0,lt=11, description="Nivel de poder (1-10)")
    incantation: str = Field(..., description="La formulación del hechizo")
    description: str = Field(..., description="Descripción del hechizo")

class SpellOut(SpellCreate):
    # Esta clase genera un ID para el hechizo creado
    spell_id:str

    class Config:
        # Con esto pydantic acepta los atributos de la clase spell
        from_atributes = True




