# schemas/residuos.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Literal

class ResiduoInput(BaseModel):
    tipo: Literal['papel', 'plastico', 'organico']
    destino: Literal['aterro', 'reciclagem', 'compostagem']
    peso_kg: float = Field(..., gt=0, description="Peso do resíduo em kg")

class ResiduoOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_calculo: datetime
    tipo: str
    destino: str
    emissao_calculada: float
    peso_kg: float