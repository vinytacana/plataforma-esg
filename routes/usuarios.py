# routes/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.usuarios import UsuarioModel
from schemas.usuarios import UsuarioCreate, UsuarioOutput, Token, TokenData
from services.auth_service import hash_senha, verificar_senha, criar_token_acesso
from config import settings
from jose import JWTError, jwt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

@router.post("/registrar", response_model=UsuarioOutput)
def registrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar se email já existe
    if db.query(UsuarioModel).filter(UsuarioModel.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Verificar se tenant_id já existe
    if db.query(UsuarioModel).filter(UsuarioModel.tenant_id == dados.tenant_id).first():
        raise HTTPException(status_code=400, detail="Tenant ID já em uso")

    novo_usuario = UsuarioModel(
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        nome_empresa=dados.nome_empresa,
        tenant_id=dados.tenant_id
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == form_data.username).first()
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = criar_token_acesso(
        data={"sub": usuario.email, "tenant_id": usuario.tenant_id}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dependência para proteger rotas
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        tenant_id: str = payload.get("tenant_id")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, tenant_id=tenant_id)
    except JWTError:
        raise credentials_exception
    
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == token_data.email).first()
    if usuario is None:
        raise credentials_exception
    return usuario

@router.get("/me", response_model=UsuarioOutput)
def ler_usuario_atual(current_user: UsuarioModel = Depends(get_current_user)):
    return current_user
