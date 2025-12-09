# services/calculo_emissoes.py
from sqlalchemy.orm import Session
from schemas.emissoes import EmissaoInput
from models.emissoes import EmissaoModel
from config import settings

def calcular_vetor_gases(atividade: float, fatores_emissao: dict) -> dict:
    """
    Substitui a antiga 'calcular_equivalente_co2'.
    Em vez de retornar um total somado, retorna o breakdown químico.
    """
    resultado = {"CO2": 0.0, "CH4": 0.0, "N2O": 0.0}
    
    if atividade <= 0:
        return resultado
        
    for gas, gwp in settings.GWP.items():
        # Pega o fator físico (kg gás / unidade)
        fe_fisico = fatores_emissao.get(gas, 0.0)
        # Calcula o impacto equivalente: Atividade * Fator * GWP
        impacto = atividade * fe_fisico * gwp
        
        if gas in resultado:
            resultado[gas] = impacto
            
    return resultado

def calcular_e_salvar_emissoes(db: Session, dados: EmissaoInput) -> EmissaoModel:
    # 1. Calcular vetores químicos para cada fonte (Gasolina, Diesel, etc)
    vetor_gasolina = calcular_vetor_gases(dados.consumo_gasolina_l, settings.FE_GASOLINA)
    vetor_diesel = calcular_vetor_gases(dados.consumo_diesel_l, settings.FE_DIESEL)
    vetor_energia = calcular_vetor_gases(dados.consumo_eletricidade_kwh, settings.FE_ELETRICIDADE_BR)
    vetor_viagem = calcular_vetor_gases(dados.viagens_km, settings.FE_VIAGEM)

    # 2. Somar por Escopo (Para o gráfico de Rosca e totais)
    escopo1 = sum(vetor_gasolina.values()) + sum(vetor_diesel.values())
    escopo2 = sum(vetor_energia.values())
    escopo3 = sum(vetor_viagem.values())
    
    total_geral = escopo1 + escopo2 + escopo3

    # 3. Somar por Gás (Para o novo gráfico Polar - Química)
    # Aqui somamos todas as fontes de CO2, todas de CH4, etc.
    soma_co2 = (vetor_gasolina["CO2"] + vetor_diesel["CO2"] + 
                vetor_energia["CO2"] + vetor_viagem["CO2"])
                
    soma_ch4 = (vetor_gasolina["CH4"] + vetor_diesel["CH4"] + 
                vetor_energia["CH4"] + vetor_viagem["CH4"])
                
    soma_n2o = (vetor_gasolina["N2O"] + vetor_diesel["N2O"] + 
                vetor_energia["N2O"] + vetor_viagem["N2O"])

    # 4. Persistência (Salvando no Banco)
    db_emissao = EmissaoModel(
        consumo_gasolina_l=dados.consumo_gasolina_l,
        consumo_diesel_l=dados.consumo_diesel_l,
        consumo_eletricidade_kwh=dados.consumo_eletricidade_kwh,
        viagens_km=dados.viagens_km,
        
        resultado_escopo1=escopo1,
        resultado_escopo2=escopo2,
        resultado_escopo3=escopo3,
        resultado_total=total_geral,
        total_co2=soma_co2,
        total_ch4=soma_ch4,
        total_n2o=soma_n2o
    )

    db.add(db_emissao)
    db.commit()
    db.refresh(db_emissao)
    
    return db_emissao