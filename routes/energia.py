# routes/energia.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.energia import EnergiaInput, EnergiaOutput
from services.calculo_energia import calcular_e_salvar_energia
from routes.usuarios import get_current_user
from models.usuarios import UsuarioModel

router = APIRouter()

@router.post("/calcular", response_model=EnergiaOutput)
def calcular_energia(
    dados: EnergiaInput, 
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Calcula indicadores de energia e salva no histórico.
    """
    return calcular_e_salvar_energia(db, dados, current_user.tenant_id)