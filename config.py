# config.py

class Settings:
    # --- 1. Configuração de Infraestrutura (RECOLOCADO) ---
    DB_URL = "sqlite:///./esg_app.db"

    # --- 2. Potencial de Aquecimento Global (GWP) - IPCC AR6 ---
    GWP = {
        "CO2": 1.0,
        "CH4": 27.9,  # Metano
        "N2O": 273.0  # Óxido Nitroso
    }

    # --- 3. Fatores de Emissão (Vetores FE_{i,g}) ---
    # Valores hipotéticos baseados no Programa Brasileiro GHG Protocol
    
    # Gasolina C (kg/litro)
    FE_GASOLINA = {
        "CO2": 2.212,
        "CH4": 0.0005,
        "N2O": 0.0001
    }
    
    # Diesel (kg/litro)
    FE_DIESEL = {
        "CO2": 2.603,
        "CH4": 0.00014,
        "N2O": 0.00005
    }

    # Eletricidade - Grid Médio BR (kg/kWh)
    FE_ELETRICIDADE_BR = {
        "CO2": 0.0450,
        "CH4": 0.00001,
        "N2O": 0.000002
    }
    
    # Viagens Aéreas (kg/km/passageiro) - Estimativa média
    FE_VIAGEM = {
        "CO2": 0.105,
        "CH4": 0.00001,
        "N2O": 0.0009
    }

    # --- NOVOS FATORES: RESÍDUOS (kg CO2e por kg de lixo) ---
    # Lógica: Aterro gera metano (alto fator). Reciclagem gasta energia mas poupa matéria-prima (baixo fator).
    FE_RESIDUOS = {
        "papel_aterro": 1.04,        # Decomposição gera metano
        "papel_reciclagem": 0.02,     # Transporte apenas
        "plastico_aterro": 0.04,     # Plástico é inerte (não apodrece, emite pouco no aterro)
        "plastico_reciclagem": 0.06, # Processo industrial de reciclagem
        "organico_aterro": 0.58,     # Muita geração de metano
        "organico_compostagem": 0.10 # Emissão controlada
    }

settings = Settings()