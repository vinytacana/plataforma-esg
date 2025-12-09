# schemas/emissoes.py
# schemas/emissoes.py
from pydantic import BaseModel, Field
from datetime import datetime

class EmissaoInput(BaseModel):
    consumo_gasolina_l: float = Field(..., ge=0, description="Litros de gasolina")
    consumo_diesel_l: float = Field(..., ge=0, description="Litros de diesel")
    consumo_eletricidade_kwh: float = Field(..., ge=0, description="kWh consumidos")
    viagens_km: float = Field(..., ge=0, description="Km rodados em viagens corporativas")

class EmissaoOutput(BaseModel):
    id: int
    data_calculo: datetime
    escopo1: float
    escopo2: float
    escopo3: float
    total: float
# --- NOVO: QUÍMICA ---
    total_co2: float
    total_ch4: float
    total_n2o: float
    class Config:
        from_attributes = True # Necessário para ler do SQLAlchemy

