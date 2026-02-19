# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict

class Settings(BaseSettings):
    # --- 1. Configuração de Infraestrutura ---
    DB_URL: str = "sqlite:///./esg_app.db"

    # --- 2. Potencial de Aquecimento Global (GWP) - IPCC AR6 ---
    GWP: Dict[str, float] = {
        "CO2": 1.0,
        "CH4": 27.9,
        "N2O": 273.0
    }

    # --- 3. Fatores de Emissão ---
    FE_GASOLINA: Dict[str, float] = {
        "CO2": 2.212,
        "CH4": 0.0005,
        "N2O": 0.0001
    }
    
    FE_DIESEL: Dict[str, float] = {
        "CO2": 2.603,
        "CH4": 0.00014,
        "N2O": 0.00005
    }

    FE_ELETRICIDADE_BR: Dict[str, float] = {
        "CO2": 0.0450,
        "CH4": 0.00001,
        "N2O": 0.000002
    }
    
    FE_VIAGEM: Dict[str, float] = {
        "CO2": 0.105,
        "CH4": 0.00001,
        "N2O": 0.0009
    }

    FE_RESIDUOS: Dict[str, float] = {
        "papel_aterro": 1.04,
        "papel_reciclagem": 0.02,
        "plastico_aterro": 0.04,
        "plastico_reciclagem": 0.06,
        "organico_aterro": 0.58,
        "organico_compostagem": 0.10
    }

    # --- 4. Mapeamento de Atividades para Escopos e Fatores ---
    # Permite refatorar os serviços para serem genéricos
    EMISSION_MAPPING: Dict[str, Dict] = {
        "consumo_gasolina_l": {"fator": "FE_GASOLINA", "escopo": 1},
        "consumo_diesel_l": {"fator": "FE_DIESEL", "escopo": 1},
        "consumo_eletricidade_kwh": {"fator": "FE_ELETRICIDADE_BR", "escopo": 2},
        "viagens_km": {"fator": "FE_VIAGEM", "escopo": 3}
    }

    # --- 5. Segurança e Autenticação ---
    SECRET_KEY: str = "super-secret-key-mudar-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
