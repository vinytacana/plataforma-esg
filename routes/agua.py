# routes/agua.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.agua import AguaInput, AguaOutput
from services.calculo_agua import registrar_consumo_agua
from models.agua import AguaModel
from routes.usuarios import get_current_user
from models.usuarios import UsuarioModel

router = APIRouter()

@router.post("/registrar", response_model=AguaOutput)
def registrar_agua(
    dados: AguaInput, 
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    return registrar_consumo_agua(db, dados, current_user.tenant_id)

@router.get("/historico", response_model=list[AguaOutput])
def listar_historico_agua(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    return db.query(AguaModel).filter(AguaModel.tenant_id == current_user.tenant_id).all()
