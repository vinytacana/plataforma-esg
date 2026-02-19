# schemas/agua.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Literal

class AguaInput(BaseModel):
    consumo_m3: float = Field(..., gt=0, description="Consumo em metros cúbicos")
    origem: Literal['rede_publica', 'poco', 'reuso'] = "rede_publica"
    preco_m3: float = Field(5.50, ge=0, description="Preço por m3 para cálculo de custo")

class AguaOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_registro: datetime
    consumo_m3: float
    origem: str
    custo_estimado: float
