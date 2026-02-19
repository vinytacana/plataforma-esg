# routes/residuos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.residuos import ResiduoInput, ResiduoOutput
from services.calculo_residuos import calcular_residuos
from models.residuos import ResiduoModel
from routes.usuarios import get_current_user
from models.usuarios import UsuarioModel

router = APIRouter()

@router.post("/calcular", response_model=ResiduoOutput)
def calcular(
    dados: ResiduoInput, 
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Calcula emissões de resíduos baseado no material e destinação final.
    """
    # Validação de Regra de Negócio Simples
    if dados.tipo == 'organico' and dados.destino == 'reciclagem':
        raise HTTPException(status_code=400, detail="Orgânico não pode ser reciclado, apenas compostado ou aterro.")

    resultado = calcular_residuos(db, dados, current_user.tenant_id)
    
    return ResiduoOutput(
        id=resultado.id,
        data_calculo=resultado.data_calculo,
        tipo=resultado.tipo,
        destino=resultado.destino,
        emissao_calculada=resultado.emissao_calculada,
        peso_kg=resultado.peso_kg
    )

@router.get("/historico", response_model=list[ResiduoOutput])
def listar_residuos(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):

    return db.query(ResiduoModel).filter(ResiduoModel.tenant_id == current_user.tenant_id).all()