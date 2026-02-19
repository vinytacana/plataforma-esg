# tests/test_agua.py
import pytest
from services.calculo_agua import registrar_consumo_agua
from schemas.agua import AguaInput

def test_registrar_consumo_agua(db_session):
    dados = AguaInput(consumo_m3=10.0, origem="rede_publica", preco_m3=5.0)
    resultado = registrar_consumo_agua(db_session, dados, "empresa-1")
    
    assert resultado.id is not None
    assert resultado.tenant_id == "empresa-1"
    assert resultado.consumo_m3 == 10.0
    assert resultado.custo_estimado == 50.0

def test_api_agua(db_session):
    from fastapi.testclient import TestClient
    from main import app
    from database import get_db
    from routes.usuarios import get_current_user
    from models.usuarios import UsuarioModel
    
    # Mocking db and user for TestClient
    mock_user = UsuarioModel(email="test@test.com", tenant_id="empresa-test", nome_empresa="Test")
    
    def override_get_db():
        yield db_session
    def override_get_current_user():
        return mock_user
        
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    client = TestClient(app)
    response = client.post("/agua/registrar", json={"consumo_m3": 20.0, "origem": "poco"})
    assert response.status_code == 200
    assert response.json()["consumo_m3"] == 20.0
