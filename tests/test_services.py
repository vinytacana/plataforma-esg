# tests/test_services.py
import pytest
from services.calculo_emissoes import calcular_vetor_gases
from config import settings

def test_calcular_vetor_gases_gasolina():
    # Testando com 100 litros de gasolina
    atividade = 100.0
    fatores = settings.FE_GASOLINA
    
    resultado = calcular_vetor_gases(atividade, fatores)
    
    # Valores esperados:
    # CO2: 100 * 2.212 * 1.0 = 221.2
    # CH4: 100 * 0.0005 * 27.9 = 1.395
    # N2O: 100 * 0.0001 * 273.0 = 2.73
    
    assert pytest.approx(resultado["CO2"]) == 221.2
    assert pytest.approx(resultado["CH4"]) == 1.395
    assert pytest.approx(resultado["N2O"]) == 2.73

def test_calcular_vetor_gases_zero():
    resultado = calcular_vetor_gases(0, settings.FE_GASOLINA)
    assert resultado == {"CO2": 0.0, "CH4": 0.0, "N2O": 0.0}

def test_calcular_vetor_gases_negativo():
    resultado = calcular_vetor_gases(-10, settings.FE_GASOLINA)
    assert resultado == {"CO2": 0.0, "CH4": 0.0, "N2O": 0.0}

from services.calculo_emissoes import calcular_e_salvar_emissoes
from schemas.emissoes import EmissaoInput

def test_calcular_e_salvar_emissoes(db_session):
    dados = EmissaoInput(
        consumo_gasolina_l=100.0,
        consumo_diesel_l=0.0,
        consumo_eletricidade_kwh=0.0,
        viagens_km=0.0
    )
    
    resultado = calcular_e_salvar_emissoes(db_session, dados, "empresa-1")
    
    assert resultado.id is not None
    assert resultado.tenant_id == "empresa-1"
    # Totais baseados no cálculo anterior
    # CO2eq = CO2*1 + CH4*27.9 + N2O*273.0
    # Gasolina 100L: 221.2 + 1.395 + 2.73 = 225.325
    assert pytest.approx(resultado.resultado_total) == 225.325

from services.calculo_energia import calcular_e_salvar_energia
from schemas.energia import EnergiaInput

def test_calcular_e_salvar_energia(db_session):
    dados = EnergiaInput(
        consumo_total_kwh=1000.0,
        consumo_renovavel_kwh=200.0,
        producao_unidades=100
    )
    
    resultado = calcular_e_salvar_energia(db_session, dados, "empresa-1")
    
    assert resultado.id is not None
    assert resultado.tenant_id == "empresa-1"
    assert resultado.percentual_renovavel == 20.0

from services.calculo_residuos import calcular_residuos
from schemas.residuos import ResiduoInput

def test_calcular_residuos(db_session):
    dados = ResiduoInput(
        tipo="papel",
        destino="aterro",
        peso_kg=100.0
    )
    
    resultado = calcular_residuos(db_session, dados, "empresa-1")
    
    assert resultado.id is not None
    assert resultado.tenant_id == "empresa-1"
    # papel_aterro: 1.04 * 100 = 104.0
    assert resultado.emissao_calculada == 104.0

from pydantic import ValidationError

def test_calcular_residuos_desconhecido(db_session):
    with pytest.raises(ValidationError):
        ResiduoInput(
            tipo="uranio",
            destino="espaco",
            peso_kg=10.0
        )
