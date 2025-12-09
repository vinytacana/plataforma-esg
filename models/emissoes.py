# models/emissoes.py
from sqlalchemy import Column, Integer, Float, DateTime, String
from database import Base
from datetime import datetime

class EmissaoModel(Base):
    __tablename__ = "emissoes"

    id = Column(Integer, primary_key=True, index=True)
    data_calculo = Column(DateTime, default=datetime.utcnow)
    
    # Inputs
    consumo_gasolina_l = Column(Float)
    consumo_diesel_l = Column(Float)
    consumo_eletricidade_kwh = Column(Float)
    viagens_km = Column(Float)
    
    # Outputs Calculados
    resultado_escopo1 = Column(Float)
    resultado_escopo2 = Column(Float)
    resultado_escopo3 = Column(Float)
    resultado_total = Column(Float)

# --- NOVO: BREAKDOWN QUÍMICO (kg CO2e) ---
    # Quanto do total veio de cada gás?
    total_co2 = Column(Float, default=0.0)
    total_ch4 = Column(Float, default=0.0)
    total_n2o = Column(Float, default=0.0)