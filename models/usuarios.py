# models/usuarios.py
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nome_empresa = Column(String, nullable=False)
    tenant_id = Column(String, unique=True, index=True, nullable=False) # Identificador único da empresa
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
