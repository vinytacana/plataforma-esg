# services/calculo_emissoes.py
from sqlalchemy.orm import Session
from schemas.emissoes import EmissaoInput
from models.emissoes import EmissaoModel
from config import settings
from typing import Dict

def calcular_vetor_gases(atividade: float, fatores_emissao: Dict[str, float]) -> Dict[str, float]:
    """Calcula o impacto químico (CO2, CH4, N2O) de uma atividade específica."""
    resultado = {"CO2": 0.0, "CH4": 0.0, "N2O": 0.0}
    
    if atividade <= 0:
        return resultado
        
    for gas, gwp in settings.GWP.items():
        fe_fisico = fatores_emissao.get(gas, 0.0)
        resultado[gas] = atividade * fe_fisico * gwp
            
    return resultado

def calcular_e_salvar_emissoes(db: Session, dados: EmissaoInput, tenant_id: str) -> EmissaoModel:
    # Inicializadores
    resultados_por_escopo = {1: 0.0, 2: 0.0, 3: 0.0}
    totais_por_gas = {"CO2": 0.0, "CH4": 0.0, "N2O": 0.0}
    
    # Itera sobre o mapeamento configurado
    for campo_input, config in settings.EMISSION_MAPPING.items():
        # Pega o valor da atividade do input (ex: dados.consumo_gasolina_l)
        atividade = getattr(dados, campo_input, 0.0)
        
        # Pega o dicionário de fatores de emissão (ex: settings.FE_GASOLINA)
        nome_fator = config["fator"]
        fatores = getattr(settings, nome_fator, {})
        
        # Calcula o vetor de gases
        vetor = calcular_vetor_gases(atividade, fatores)
        
        # Acumula por escopo
        escopo = config["escopo"]
        resultados_por_escopo[escopo] += sum(vetor.values())
        
        # Acumula por gás
        for gas in totais_por_gas:
            totais_por_gas[gas] += vetor[gas]

    total_geral = sum(resultados_por_escopo.values())

    # Persistência
    db_emissao = EmissaoModel(
        tenant_id=tenant_id,
        consumo_gasolina_l=dados.consumo_gasolina_l,
        consumo_diesel_l=dados.consumo_diesel_l,
        consumo_eletricidade_kwh=dados.consumo_eletricidade_kwh,
        viagens_km=dados.viagens_km,
        
        resultado_escopo1=resultados_por_escopo[1],
        resultado_escopo2=resultados_por_escopo[2],
        resultado_escopo3=resultados_por_escopo[3],
        resultado_total=total_geral,
        
        total_co2=totais_por_gas["CO2"],
        total_ch4=totais_por_gas["CH4"],
        total_n2o=totais_por_gas["N2O"]
    )

    db.add(db_emissao)
    db.commit()
    db.refresh(db_emissao)
    
    return db_emissao
