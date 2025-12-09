# routes/emissoes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.emissoes import EmissaoInput, EmissaoOutput
from services.calculo_emissoes import calcular_e_salvar_emissoes
from database import get_db

router = APIRouter()

@router.post("/calcular", response_model=EmissaoOutput)
def calcular_emissao(dados: EmissaoInput, db: Session = Depends(get_db)):
    """
    Calcula emissões e salva o registro no histórico.
    """
    resultado_db = calcular_e_salvar_emissoes(db, dados)
    
    # Mapeamento do Model para o Schema de Saída
    return EmissaoOutput(
        id=resultado_db.id,
        data_calculo=resultado_db.data_calculo,
        escopo1=resultado_db.resultado_escopo1,
        escopo2=resultado_db.resultado_escopo2,
        escopo3=resultado_db.resultado_escopo3,
        total=resultado_db.resultado_total
    )

@router.get("/historico", response_model=list[EmissaoOutput])
def listar_historico(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Nova rota para consultar cálculos passados
    from models.emissoes import EmissaoModel # Import local para evitar ciclo
    registros = db.query(EmissaoModel).offset(skip).limit(limit).all()
    # Conversão manual ou automática via Pydantic
    return [
        EmissaoOutput(
            id=r.id, data_calculo=r.data_calculo,
            escopo1=r.resultado_escopo1, escopo2=r.resultado_escopo2,
            escopo3=r.resultado_escopo3, total=r.resultado_total
        ) for r in registros
    ]