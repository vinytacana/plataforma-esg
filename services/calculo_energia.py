# services/calculo_energia.py
from sqlalchemy.orm import Session
from schemas.energia import EnergiaInput
from models.energia import EnergiaModel
from config import settings

def calcular_e_salvar_energia(db: Session, dados: EnergiaInput) -> EnergiaModel:
    
    # --- 1. Cálculos de Performance Energética ---
    percentual_renovavel = 0.0
    if dados.consumo_total_kwh > 0:
        percentual_renovavel = (dados.consumo_renovavel_kwh / dados.consumo_total_kwh) * 100
        
    intensidade = 0.0
    if dados.producao_unidades > 0:
        intensidade = dados.consumo_total_kwh / dados.producao_unidades

    # --- 2. Cálculo Estequiométrico ---
    atividade_A = dados.consumo_total_kwh
    fator_composto = 0.0
    
    for gas, gwp in settings.GWP.items():
        fe_gas = settings.FE_ELETRICIDADE_BR.get(gas, 0.0)
        fator_composto += fe_gas * gwp 

    emissao_total_kg = atividade_A * fator_composto
    emissao_total_t = emissao_total_kg / 1000.0

    # --- 3. Persistência (CORRIGIDO) ---
    db_energia = EnergiaModel(
        consumo_total=dados.consumo_total_kwh,
        consumo_renovavel=dados.consumo_renovavel_kwh,
        producao_unidades=dados.producao_unidades,
        
        # Aqui mudamos os nomes dos argumentos para bater com o novo Model
        percentual_renovavel=percentual_renovavel, 
        intensidade=intensidade,
        
        emissoes_totais_tco2e=emissao_total_t 
    )

    db.add(db_energia)
    db.commit()
    db.refresh(db_energia)
    
    return db_energia