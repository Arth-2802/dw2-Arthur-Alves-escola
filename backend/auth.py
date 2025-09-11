"""
Módulo de autenticação para o Sistema de Gestão Escolar
Implementa JWT tokens, hash de senhas e verificação de usuários
"""
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models import Usuario
from database import get_db

# Configurações de segurança
SECRET_KEY = "escola_secret_key_2024_muito_segura"  # Em produção, usar variável de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 horas

# Configuração do hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticação Bearer Token
security = HTTPBearer()

def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """
    Verifica se a senha fornecida confere com o hash armazenado
    """
    return pwd_context.verify(senha_pura, senha_hash)

def criar_hash_senha(senha: str) -> str:
    """
    Cria um hash da senha para armazenamento seguro
    """
    return pwd_context.hash(senha)

def criar_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cria um JWT token de acesso
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def autenticar_usuario(db: Session, username: str, senha: str) -> Optional[Usuario]:
    """
    Autentica um usuário verificando username e senha
    """
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if not usuario:
        return None
    if not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario

async def obter_usuario_atual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtém o usuário atual a partir do token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica o token JWT
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Busca o usuário no banco
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario is None:
        raise credentials_exception
    
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo"
        )
    
    return usuario

def usuario_ativo_required(usuario: Usuario = Depends(obter_usuario_atual)) -> Usuario:
    """
    Dependency que exige um usuário ativo
    """
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo"
        )
    return usuario
