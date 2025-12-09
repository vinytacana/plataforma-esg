# schemas/energia.py
from pydantic import BaseModel, Field
from datetime import datetime

class EnergiaInput(BaseModel):
    consumo_total_kwh: float = Field(..., ge=0, description="Dado de atividade A_i (kWh)")
    consumo_renovavel_kwh: float = Field(..., ge=0)
    producao_unidades: float = Field(..., ge=0)

class EnergiaOutput(BaseModel):
    id: int
    data_calculo: datetime
    percentual_renovavel: float
    intensidade: float
    emissoes_totais_tco2e: float # Resultado da equação do manual

    class Config:
        from_attributes = True