# routes/relatorios.py
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models.emissoes import EmissaoModel
from models.residuos import ResiduoModel
from services.relatorio_service import (
    gerar_pdf_ghg, 
    gerar_plano_descarbonizacao, 
    gerar_csv_auditoria
)

router = APIRouter()

@router.get("/ghg-protocol")
def baixar_relatorio_tecnico(db: Session = Depends(get_db)):
    emissoes = db.query(EmissaoModel).all()
    arquivo = gerar_pdf_ghg(emissoes)
    return FileResponse(arquivo, filename="Relatorio_GHG_2024.pdf", media_type='application/pdf')

@router.get("/plano-descarbonizacao")
def baixar_plano_estrategico(db: Session = Depends(get_db)):
    emissoes = db.query(EmissaoModel).all()

    arquivo = gerar_plano_descarbonizacao(emissoes)
    return FileResponse(arquivo, filename="Plano_Descarbonizacao_2030.pdf", media_type='application/pdf')

@router.get("/auditoria-compliance")
def baixar_csv_compliance(db: Session = Depends(get_db)):
    emissoes = db.query(EmissaoModel).all()
    residuos = db.query(ResiduoModel).all()
    
    arquivo = gerar_csv_auditoria(emissoes, residuos)
    return FileResponse(arquivo, filename="Auditoria_Conformidade.csv", media_type='text/csv')