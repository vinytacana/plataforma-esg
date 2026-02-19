# tests/test_metricas.py
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
from models.metricas import MetricaModel
from models.usuarios import UsuarioModel
from routes.usuarios import get_current_user

client = TestClient(app)

def test_registrar_metrica_social(db_session):
    # Mocking db and user for TestClient
    mock_user = UsuarioModel(email="test@test.com", tenant_id="empresa-test", nome_empresa="Test")
    def override_get_db():
        yield db_session
    def override_get_current_user():
        return mock_user
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    payload = {
        "categoria": "social",
        "nome": "diversidade_lideranca",
        "valor": 45.5,
        "unidade": "%",
        "descricao": "Percentual de mulheres em cargos de liderança"
    }
    response = client.post("/metricas/registrar", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "diversidade_lideranca"
    assert data["valor"] == 45.5

def test_listar_metricas_por_categoria(db_session):
    mock_user = UsuarioModel(email="test@test.com", tenant_id="social-tenant", nome_empresa="Test")
    def override_get_db():
        yield db_session
    def override_get_current_user():
        return mock_user
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    # Criar uma social e uma governança DIRETAMENTE no banco
    m1 = MetricaModel(categoria="social", nome="s1", valor=10, tenant_id="social-tenant")
    m2 = MetricaModel(categoria="governanca", nome="g1", valor=20, tenant_id="social-tenant")
    db_session.add(m1)
    db_session.add(m2)
    db_session.commit()
    
    # Filtrar por social
    response = client.get("/metricas/historico?categoria=social")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["categoria"] == "social"
