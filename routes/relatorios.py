# routes/relatorios.py
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models.emissoes import EmissaoModel
from models.energia import EnergiaModel
from services.relatorio_service import gerar_csv_consolidado, gerar_pdf_certificado

router = APIRouter()

@router.get("/exportar-csv")
def exportar_csv(db: Session = Depends(get_db)):
    """
    Baixa um CSV com todo o histórico combinado (Data Science Ready).
    """
    emissoes = db.query(EmissaoModel).all()
    energia = db.query(EnergiaModel).all()
    
    arquivo = gerar_csv_consolidado(emissoes, energia)
    return FileResponse(arquivo, filename="relatorio_esg_completo.csv", media_type='text/csv')

@router.get("/gerar-certificado")
def baixar_certificado(db: Session = Depends(get_db)):
    """
    Gera um PDF oficial com totais e metodologia científica.
    """
    emissoes = db.query(EmissaoModel).all()
    energia = db.query(EnergiaModel).all()
    
    arquivo = gerar_pdf_certificado(emissoes, energia)
    return FileResponse(arquivo, filename="certificado_esg.pdf", media_type='application/pdf')