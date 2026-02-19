# routes/metricas.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from schemas.metricas import MetricaInput, MetricaOutput
from models.metricas import MetricaModel
from routes.usuarios import get_current_user
from models.usuarios import UsuarioModel

router = APIRouter()

@router.post("/registrar", response_model=MetricaOutput)
def registrar_metrica(
    dados: MetricaInput, 
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    db_obj = MetricaModel(
        tenant_id=current_user.tenant_id,
        categoria=dados.categoria,
        nome=dados.nome,
        valor=dados.valor,
        unidade=dados.unidade,
        descricao=dados.descricao
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/historico", response_model=list[MetricaOutput])
def listar_metricas(
    categoria: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    query = db.query(MetricaModel).filter(MetricaModel.tenant_id == current_user.tenant_id)
    if categoria:
        query = query.filter(MetricaModel.categoria == categoria)
    return query.offset(skip).limit(limit).all()
