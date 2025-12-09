# routes/emissoes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.emissoes import EmissaoInput, EmissaoOutput
from services.calculo_emissoes import calcular_e_salvar_emissoes
from database import get_db
from models.emissoes import EmissaoModel

router = APIRouter()

@router.post("/calcular", response_model=EmissaoOutput)
def calcular_emissao(dados: EmissaoInput, db: Session = Depends(get_db)):
  
    resultado_db = calcular_e_salvar_emissoes(db, dados)
    
    return EmissaoOutput(
        id=resultado_db.id,
        data_calculo=resultado_db.data_calculo,
        escopo1=resultado_db.resultado_escopo1,
        escopo2=resultado_db.resultado_escopo2,
        escopo3=resultado_db.resultado_escopo3,
        total=resultado_db.resultado_total,
        # --- CAMPOS QUÍMICOS NOVOS ---
        total_co2=resultado_db.total_co2,
        total_ch4=resultado_db.total_ch4,
        total_n2o=resultado_db.total_n2o
    )

@router.get("/historico", response_model=list[EmissaoOutput])
def listar_historico(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    registros = db.query(EmissaoModel).offset(skip).limit(limit).all()

    return [
        EmissaoOutput(
            id=r.id,
            data_calculo=r.data_calculo,
            escopo1=r.resultado_escopo1,
            escopo2=r.resultado_escopo2,
            escopo3=r.resultado_escopo3,
            total=r.resultado_total,
            total_co2=r.total_co2,
            total_ch4=r.total_ch4,
            total_n2o=r.total_n2o,
        ) for r in registros
    ]