# services/calculo_agua.py
from sqlalchemy.orm import Session
from schemas.agua import AguaInput
from models.agua import AguaModel

def registrar_consumo_agua(db: Session, dados: AguaInput, tenant_id: str) -> AguaModel:
    # Cálculo simples de custo
    custo = dados.consumo_m3 * dados.preco_m3
    
    db_obj = AguaModel(
        tenant_id=tenant_id,
        consumo_m3=dados.consumo_m3,
        origem=dados.origem,
        custo_estimado=custo
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    return db_obj
