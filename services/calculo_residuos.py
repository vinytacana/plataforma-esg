# services/calculo_residuos.py
from sqlalchemy.orm import Session
from schemas.residuos import ResiduoInput
from models.residuos import ResiduoModel
from config import settings

def calcular_residuos(db: Session, dados: ResiduoInput) -> ResiduoModel:
    # 1. Monta a chave para buscar no config (ex: "papel_aterro")
    chave_fator = f"{dados.tipo}_{dados.destino}"
    
    # 2. Busca o fator (se não existir, usa 0.0 e avisa no log)
    fator = settings.FE_RESIDUOS.get(chave_fator, 0.0)
    
    # 3. Cálculo: E = Massa * Fator
    emissao_total = dados.peso_kg * fator

    # 4. Salva no Banco
    db_obj = ResiduoModel(
        tipo=dados.tipo,
        destino=dados.destino,
        peso_kg=dados.peso_kg,
        emissao_calculada=emissao_total
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    return db_obj