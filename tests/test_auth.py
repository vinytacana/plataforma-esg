# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db

client = TestClient(app)

def test_registrar_e_login(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    
    # 1. Registrar
    user_data = {
        "email": "test@empresa.com",
        "senha": "password123",
        "nome_empresa": "Empresa Teste",
        "tenant_id": "empresa-1"
    }
    response = client.post("/usuarios/registrar", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test@empresa.com"
    
    # 2. Login
    login_data = {
        "username": "test@empresa.com",
        "password": "password123"
    }
    response = client.post("/usuarios/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalido(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    
    login_data = {
        "username": "errado@teste.com",
        "password": "senha"
    }
    response = client.post("/usuarios/login", data=login_data)
    assert response.status_code == 401
