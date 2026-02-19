# tests/test_api.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app
from fastapi.testclient import TestClient
from models.usuarios import UsuarioModel
from routes.usuarios import get_current_user

# Setup do banco de dados de teste para a API usando StaticPool para persistência em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_read_main():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307

def test_isolamento_multi_tenant(db_session):
    # 1. Criar dois usuários de empresas diferentes
    user1 = UsuarioModel(email="u1@test.com", tenant_id="T1", nome_empresa="Empresa 1")
    user2 = UsuarioModel(email="u2@test.com", tenant_id="T2", nome_empresa="Empresa 2")
    
    # Mock do banco para o TestClient usar o db_session do fixture
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db

    # 2. Registrar dados como Usuário 1
    app.dependency_overrides[get_current_user] = lambda: user1
    client.post("/emissoes/calcular", json={
        "consumo_gasolina_l": 100.0, "consumo_diesel_l": 0.0,
        "consumo_eletricidade_kwh": 0.0, "viagens_km": 0.0
    })

    # 3. Verificar que Usuário 1 VÊ seu dado
    response1 = client.get("/emissoes/historico")
    assert len(response1.json()) == 1

    # 4. Verificar que Usuário 2 NÃO VÊ o dado do Usuário 1
    app.dependency_overrides[get_current_user] = lambda: user2
    response2 = client.get("/emissoes/historico")
    assert len(response2.json()) == 0
