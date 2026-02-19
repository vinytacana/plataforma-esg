# schemas/metricas.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Literal

class MetricaInput(BaseModel):
    categoria: Literal['social', 'governanca', 'ambiental']
    nome: str = Field(..., min_length=3, description="Nome do indicador")
    valor: float
    unidade: Optional[str] = None
    descricao: Optional[str] = None

class MetricaOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_registro: datetime
    categoria: str
    nome: str
    valor: float
    unidade: Optional[str]
    descricao: Optional[str]
