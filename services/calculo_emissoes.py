# services/calculo_emissoes.py
from sqlalchemy.orm import Session
from schemas.emissoes import EmissaoInput
from models.emissoes import EmissaoModel
from config import settings

def calcular_equivalente_co2(atividade: float, fatores_emissao: dict) -> float:
    if atividade <= 0: return 0.0
    fator_composto = 0.0
    for gas, gwp in settings.GWP.items():
        fe = fatores_emissao.get(gas, 0.0)
        fator_composto += fe * gwp
    return atividade * fator_composto

def calcular_e_salvar_emissoes(db: Session, dados: EmissaoInput) -> EmissaoModel:
    # Note que agora usamos FE_GASOLINA (Dicionário), não FATOR_GASOLINA
    emissao_gasolina = calcular_equivalente_co2(dados.consumo_gasolina_l, settings.FE_GASOLINA)
    emissao_diesel = calcular_equivalente_co2(dados.consumo_diesel_l, settings.FE_DIESEL)
    
    escopo1_kg = emissao_gasolina + emissao_diesel
    escopo2_kg = calcular_equivalente_co2(dados.consumo_eletricidade_kwh, settings.FE_ELETRICIDADE_BR)
    escopo3_kg = calcular_equivalente_co2(dados.viagens_km, settings.FE_VIAGEM)
    
    total_kg = escopo1_kg + escopo2_kg + escopo3_kg

    db_emissao = EmissaoModel(
        consumo_gasolina_l=dados.consumo_gasolina_l,
        consumo_diesel_l=dados.consumo_diesel_l,
        consumo_eletricidade_kwh=dados.consumo_eletricidade_kwh,
        viagens_km=dados.viagens_km,
        resultado_escopo1=escopo1_kg,
        resultado_escopo2=escopo2_kg,
        resultado_escopo3=escopo3_kg,
        resultado_total=total_kg
    )
    db.add(db_emissao)
    db.commit()
    db.refresh(db_emissao)
    return db_emissao