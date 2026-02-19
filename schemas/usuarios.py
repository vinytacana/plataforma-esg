# schemas/usuarios.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UsuarioBase(BaseModel):
    email: EmailStr
    nome_empresa: str
    tenant_id: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioOutput(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    is_admin: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    tenant_id: Optional[str] = None
