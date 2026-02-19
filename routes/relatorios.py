# routes/relatorios.py
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models.emissoes import EmissaoModel
from models.residuos import ResiduoModel
from models.agua import AguaModel
from models.energia import EnergiaModel
from models.metricas import MetricaModel
from services.relatorio_service import (
    gerar_pdf_ghg, 
    gerar_relatorio_executivo, 
    gerar_csv_auditoria
)

from models.usuarios import UsuarioModel
from routes.usuarios import get_current_user

router = APIRouter()

@router.get("/executivo")
def baixar_relatorio_consolidado(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    emissoes = db.query(EmissaoModel).filter(EmissaoModel.tenant_id == current_user.tenant_id).all()
    residuos = db.query(ResiduoModel).filter(ResiduoModel.tenant_id == current_user.tenant_id).all()
    agua = db.query(AguaModel).filter(AguaModel.tenant_id == current_user.tenant_id).all()
    energia = db.query(EnergiaModel).filter(EnergiaModel.tenant_id == current_user.tenant_id).all()
    metricas = db.query(MetricaModel).filter(MetricaModel.tenant_id == current_user.tenant_id).all()
    
    arquivo = gerar_relatorio_executivo(emissoes, agua, residuos, energia, metricas)
    return FileResponse(arquivo, filename=f"Relatorio_Executivo_{current_user.tenant_id}.pdf", media_type='application/pdf')

@router.get("/ghg-protocol")
def baixar_relatorio_tecnico(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    emissoes = db.query(EmissaoModel).filter(EmissaoModel.tenant_id == current_user.tenant_id).all()
    arquivo = gerar_pdf_ghg(emissoes)
    return FileResponse(arquivo, filename=f"Relatorio_GHG_{current_user.tenant_id}.pdf", media_type='application/pdf')

@router.get("/auditoria-compliance")
def baixar_csv_compliance(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    emissoes = db.query(EmissaoModel).filter(EmissaoModel.tenant_id == current_user.tenant_id).all()
    residuos = db.query(ResiduoModel).filter(ResiduoModel.tenant_id == current_user.tenant_id).all()
    
    arquivo = gerar_csv_auditoria(emissoes, residuos)
    return FileResponse(arquivo, filename=f"Auditoria_{current_user.tenant_id}.csv", media_type='text/csv')
