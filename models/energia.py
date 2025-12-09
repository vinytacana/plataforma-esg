# models/energia.py
from sqlalchemy import Column, Integer, Float, DateTime
from database import Base
from datetime import datetime

class EnergiaModel(Base):
    __tablename__ = "energia"

    id = Column(Integer, primary_key=True, index=True)
    data_calculo = Column(DateTime, default=datetime.utcnow)
    
    # Inputs
    consumo_total = Column(Float)
    consumo_renovavel = Column(Float)
    producao_unidades = Column(Float)
    
    # Outputs (NOMES CORRIGIDOS PARA BATER COM O SCHEMA)
    percentual_renovavel = Column(Float)  # Antes era resultado_percentual_renovavel
    intensidade = Column(Float)           # Antes era resultado_intensidade
    
    # Output Científico
    emissoes_totais_tco2e = Column(Float)