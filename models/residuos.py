# models/residuos.py
from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base
from datetime import datetime

class ResiduoModel(Base):
    __tablename__ = "residuos"

    id = Column(Integer, primary_key=True, index=True)
    data_calculo = Column(DateTime, default=datetime.utcnow)
    
    tipo = Column(String)
    destino = Column(String)
    peso_kg = Column(Float)
    
    # O resultado do cálculo
    emissao_calculada = Column(Float)