# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # NOVO: Importar isso
from fastapi.responses import RedirectResponse # NOVO: Para redirecionar a home
from database import engine, Base
import models.emissoes 
import models.energia
import models.residuos
from routes import emissoes, energia, relatorios, residuos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Calculadora ESG Enterprise")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# --- ROTAS DA API ---
app.include_router(emissoes.router, prefix="/emissoes", tags=["Emissões"])
app.include_router(energia.router, prefix="/energia", tags=["Energia"])
app.include_router(relatorios.router, prefix="/relatorios", tags=["Relatórios"])
app.include_router(residuos.router, prefix="/residuos", tags=["Resíduos"])

# --- NOVO: SERVIR O FRONT-END ---
# Isso faz com que seus arquivos HTML fiquem acessíveis
app.mount("/app", StaticFiles(directory="static", html=True), name="static")

# Redirecionar a raiz (/) para o index.html
@app.get("/")
def home():
    return RedirectResponse(url="/app/index.html")