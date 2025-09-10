"""
API FastAPI para Sistema de Gestão Escolar
Implementa endpoints REST para gerenciar alunos, turmas e matrículas
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
import datetime
import re

# Importações locais
from database import SessionLocal, engine, get_db
from models import Base, Aluno, Turma

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicialização da aplicação FastAPI
app = FastAPI(
    title="Sistema de Gestão Escolar",
    description="API REST para gerenciamento de alunos, turmas e matrículas",
    version="1.0.0"
)

# Configuração CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === SCHEMAS PYDANTIC ===
# Modelos para validação de entrada e saída da API

class TurmaBase(BaseModel):
    """Schema base para Turma"""
    nome: str = Field(..., min_length=1, max_length=100, description="Nome da turma")
    capacidade: int = Field(..., gt=0, le=50, description="Capacidade máxima da turma")

class TurmaCreate(TurmaBase):
    """Schema para criação de turma"""
    pass

class TurmaResponse(TurmaBase):
    """Schema para resposta com turma"""
    id: int
    ocupacao: int = 0  # Será calculado dinamicamente
    
    model_config = {"from_attributes": True}

class AlunoBase(BaseModel):
    """Schema base para Aluno"""
    nome: str = Field(..., min_length=3, max_length=80, description="Nome do aluno")
    data_nascimento: datetime.date = Field(..., description="Data de nascimento")
    email: Optional[str] = Field(None, max_length=255, description="Email do aluno")
    status: str = Field("inativo", pattern="^(ativo|inativo)$", description="Status do aluno")
    turma_id: Optional[int] = Field(None, description="ID da turma")
    
    @field_validator('data_nascimento')
    @classmethod
    def validar_idade_minima(cls, v):
        """Valida se o aluno tem pelo menos 5 anos"""
        hoje = datetime.date.today()
        idade = hoje.year - v.year - ((hoje.month, hoje.day) < (v.month, v.day))
        if idade < 5:
            raise ValueError('Aluno deve ter pelo menos 5 anos de idade')
        return v
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        """Valida formato do email"""
        if v is not None and v.strip():
            padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(padrao_email, v):
                raise ValueError('Formato de email inválido')
        return v

class AlunoCreate(AlunoBase):
    """Schema para criação de aluno"""
    pass

class AlunoUpdate(BaseModel):
    """Schema para atualização de aluno (campos opcionais)"""
    nome: Optional[str] = Field(None, min_length=3, max_length=80)
    data_nascimento: Optional[datetime.date] = None
    email: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, pattern="^(ativo|inativo)$")
    turma_id: Optional[int] = None
    
    @field_validator('data_nascimento')
    @classmethod
    def validar_idade_minima(cls, v):
        if v is not None:
            hoje = datetime.date.today()
            idade = hoje.year - v.year - ((hoje.month, hoje.day) < (v.month, v.day))
            if idade < 5:
                raise ValueError('Aluno deve ter pelo menos 5 anos de idade')
        return v
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        if v is not None and v.strip():
            padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(padrao_email, v):
                raise ValueError('Formato de email inválido')
        return v

class AlunoResponse(AlunoBase):
    """Schema para resposta com aluno"""
    id: int
    idade: int = 0  # Será calculado dinamicamente
    turma_nome: Optional[str] = None  # Nome da turma
    
    model_config = {"from_attributes": True}

class MatriculaRequest(BaseModel):
    """Schema para solicitação de matrícula"""
    aluno_id: int = Field(..., description="ID do aluno")
    turma_id: int = Field(..., description="ID da turma")

# === ENDPOINTS ===

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Sistema de Gestão Escolar API",
        "version": "1.0.0",
        "endpoints": {
            "alunos": "/alunos",
            "turmas": "/turmas",
            "matriculas": "/matriculas"
        }
    }

# === ENDPOINTS DE TURMAS ===

@app.get("/turmas", response_model=List[TurmaResponse], tags=["Turmas"])
def listar_turmas(db: Session = Depends(get_db)):
    """
    Lista todas as turmas com informação de ocupação
    """
    turmas = db.query(Turma).all()
    resultado = []
    
    for turma in turmas:
        ocupacao = db.query(Aluno).filter(
            Aluno.turma_id == turma.id,
            Aluno.status == "ativo"
        ).count()
        
        turma_dict = {
            "id": turma.id,
            "nome": turma.nome,
            "capacidade": turma.capacidade,
            "ocupacao": ocupacao
        }
        resultado.append(turma_dict)
    
    return resultado

@app.post("/turmas", response_model=TurmaResponse, status_code=201, tags=["Turmas"])
def criar_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova turma
    """
    # Verifica se já existe turma com mesmo nome
    turma_existente = db.query(Turma).filter(Turma.nome == turma.nome).first()
    if turma_existente:
        raise HTTPException(status_code=400, detail="Turma com este nome já existe")
    
    db_turma = Turma(**turma.dict())
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    
    return {
        "id": db_turma.id,
        "nome": db_turma.nome,
        "capacidade": db_turma.capacidade,
        "ocupacao": 0
    }

# === ENDPOINTS DE ALUNOS ===

@app.get("/alunos", response_model=List[AlunoResponse], tags=["Alunos"])
def listar_alunos(
    search: Optional[str] = Query(None, description="Busca por nome"),
    turma_id: Optional[int] = Query(None, description="Filtro por turma"),
    status: Optional[str] = Query(None, description="Filtro por status"),
    db: Session = Depends(get_db)
):
    """
    Lista alunos com filtros opcionais por nome, turma e status
    """
    query = db.query(Aluno)
    
    # Aplicar filtros
    if search:
        query = query.filter(Aluno.nome.ilike(f"%{search}%"))
    
    if turma_id:
        query = query.filter(Aluno.turma_id == turma_id)
    
    if status:
        query = query.filter(Aluno.status == status)
    
    alunos = query.all()
    resultado = []
    
    for aluno in alunos:
        turma_nome = None
        if aluno.turma:
            turma_nome = aluno.turma.nome
        
        aluno_dict = {
            "id": aluno.id,
            "nome": aluno.nome,
            "data_nascimento": aluno.data_nascimento,
            "email": aluno.email,
            "status": aluno.status,
            "turma_id": aluno.turma_id,
            "idade": aluno.idade,
            "turma_nome": turma_nome
        }
        resultado.append(aluno_dict)
    
    return resultado

@app.post("/alunos", response_model=AlunoResponse, status_code=201, tags=["Alunos"])
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo aluno
    """
    # Verifica se email já existe (se fornecido)
    if aluno.email:
        aluno_existente = db.query(Aluno).filter(Aluno.email == aluno.email).first()
        if aluno_existente:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Verifica se turma existe (se fornecida)
    if aluno.turma_id:
        turma = db.query(Turma).filter(Turma.id == aluno.turma_id).first()
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    db_aluno = Aluno(**aluno.dict())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    
    turma_nome = None
    if db_aluno.turma:
        turma_nome = db_aluno.turma.nome
    
    return {
        "id": db_aluno.id,
        "nome": db_aluno.nome,
        "data_nascimento": db_aluno.data_nascimento,
        "email": db_aluno.email,
        "status": db_aluno.status,
        "turma_id": db_aluno.turma_id,
        "idade": db_aluno.idade,
        "turma_nome": turma_nome
    }

@app.put("/alunos/{aluno_id}", response_model=AlunoResponse, tags=["Alunos"])
def atualizar_aluno(aluno_id: int, aluno: AlunoUpdate, db: Session = Depends(get_db)):
    """
    Atualiza dados de um aluno existente
    """
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Verifica email único (se alterado)
    if aluno.email and aluno.email != db_aluno.email:
        aluno_existente = db.query(Aluno).filter(Aluno.email == aluno.email).first()
        if aluno_existente:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Verifica se turma existe (se fornecida)
    if aluno.turma_id:
        turma = db.query(Turma).filter(Turma.id == aluno.turma_id).first()
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    # Atualiza apenas campos fornecidos
    dados_atualizacao = aluno.dict(exclude_unset=True)
    for campo, valor in dados_atualizacao.items():
        setattr(db_aluno, campo, valor)
    
    db.commit()
    db.refresh(db_aluno)
    
    turma_nome = None
    if db_aluno.turma:
        turma_nome = db_aluno.turma.nome
    
    return {
        "id": db_aluno.id,
        "nome": db_aluno.nome,
        "data_nascimento": db_aluno.data_nascimento,
        "email": db_aluno.email,
        "status": db_aluno.status,
        "turma_id": db_aluno.turma_id,
        "idade": db_aluno.idade,
        "turma_nome": turma_nome
    }

@app.delete("/alunos/{aluno_id}", tags=["Alunos"])
def excluir_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """
    Exclui um aluno
    """
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    db.delete(db_aluno)
    db.commit()
    
    return {"message": "Aluno excluído com sucesso"}

# === ENDPOINT DE MATRÍCULA ===

@app.post("/matriculas", tags=["Matrículas"])
def matricular_aluno(matricula: MatriculaRequest, db: Session = Depends(get_db)):
    """
    Matricula um aluno em uma turma
    Valida capacidade e altera status para ativo
    """
    # Busca aluno
    aluno = db.query(Aluno).filter(Aluno.id == matricula.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Busca turma
    turma = db.query(Turma).filter(Turma.id == matricula.turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    # Verifica capacidade da turma
    ocupacao_atual = db.query(Aluno).filter(
        Aluno.turma_id == turma.id,
        Aluno.status == "ativo"
    ).count()
    
    if ocupacao_atual >= turma.capacidade:
        raise HTTPException(
            status_code=422, 
            detail=f"Turma '{turma.nome}' já atingiu capacidade máxima ({turma.capacidade} alunos)"
        )
    
    # Realiza matrícula
    aluno.turma_id = turma.id
    aluno.status = "ativo"  # Altera status automaticamente
    
    db.commit()
    
    return {
        "message": f"Aluno '{aluno.nome}' matriculado na turma '{turma.nome}' com sucesso",
        "aluno_id": aluno.id,
        "turma_id": turma.id,
        "novo_status": aluno.status
    }

# Executar servidor se executado diretamente
if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor da API...")
    print("📍 URL: http://localhost:8001")
    print("📖 Documentação: http://localhost:8001/docs")
    print("⚡ Servidor executando...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
