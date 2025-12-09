# schemas/residuos.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class ResiduoInput(BaseModel):
    tipo: Literal['papel', 'plastico', 'organico']
    destino: Literal['aterro', 'reciclagem', 'compostagem']
    peso_kg: float = Field(..., gt=0, description="Peso do resíduo em kg")

class ResiduoOutput(BaseModel):
    id: int
    data_calculo: datetime
    tipo: str
    destino: str
    emissao_calculada: float
    peso_kg: float

    class Config:
        from_attributes = True