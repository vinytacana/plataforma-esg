# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # NOVO: Importar isso
from fastapi.responses import RedirectResponse # NOVO: Para redirecionar a home
from database import engine, Base
import models.emissoes 
import models.energia
import models.residuos
import models.agua
import models.metricas
import models.usuarios
from routes import emissoes, energia, relatorios, residuos, agua, metricas, usuarios

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Calculadora ESG Enterprise")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# --- ROTAS DA API ---
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários e Autenticação"])
app.include_router(emissoes.router, prefix="/emissoes", tags=["Emissões"])
app.include_router(energia.router, prefix="/energia", tags=["Energia"])
app.include_router(relatorios.router, prefix="/relatorios", tags=["Relatórios"])
app.include_router(residuos.router, prefix="/residuos", tags=["Resíduos"])
app.include_router(agua.router, prefix="/agua", tags=["Água"])
app.include_router(metricas.router, prefix="/metricas", tags=["Métricas Gerais (S/G)"])


app.mount("/app", StaticFiles(directory="static", html=True), name="static")

@app.get("/")

def home():

    return RedirectResponse(url="/app/login.html")
