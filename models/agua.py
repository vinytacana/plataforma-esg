# models/agua.py
from sqlalchemy import Column, Integer, Float, DateTime, String
from database import Base
from datetime import datetime

class AguaModel(Base):
    __tablename__ = "consumo_agua"

    id = Column(Integer, primary_key=True, index=True)
    data_registro = Column(DateTime, default=datetime.utcnow)
    tenant_id = Column(String, index=True, nullable=False)
    
    consumo_m3 = Column(Float, nullable=False)
    origem = Column(String, default="rede_publica") # rede_publica, poco, reuso
    custo_estimado = Column(Float, default=0.0)
