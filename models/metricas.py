# models/metricas.py
from sqlalchemy import Column, Integer, Float, DateTime, String, Enum
from database import Base
from datetime import datetime
import enum

class CategoriaMetrica(str, enum.Enum):
    SOCIAL = "social"
    GOVERNANCA = "governanca"
    AMBIENTAL = "ambiental" # Para métricas simples não-químicas

class MetricaModel(Base):
    __tablename__ = "metricas_esg"

    id = Column(Integer, primary_key=True, index=True)
    data_registro = Column(DateTime, default=datetime.utcnow)
    tenant_id = Column(String, index=True, nullable=False)
    
    categoria = Column(String, nullable=False) # social, governanca
    nome = Column(String, nullable=False) # ex: diversidade_lideranca, treinamentos_etica
    valor = Column(Float, nullable=False)
    unidade = Column(String, nullable=True) # %, horas, pessoas, etc.
    descricao = Column(String, nullable=True)
