from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date, datetime
from database import get_db, engine
import models
from pydantic import BaseModel, validator
from dateutil.relativedelta import relativedelta

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Escola API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TurmaBase(BaseModel):
    nome: str
    capacidade: int

    @validator('capacidade')
    def validate_capacidade(cls, v):
        if v < 1:
            raise ValueError('Capacidade deve ser maior que zero')
        return v

class AlunoBase(BaseModel):
    nome: str
    data_nascimento: date
    email: Optional[str] = None
    status: models.StatusEnum = models.StatusEnum.INATIVO
    turma_id: Optional[int] = None

    @validator('nome')
    def validate_nome(cls, v):
        if len(v) < 3 or len(v) > 80:
            raise ValueError('Nome deve ter entre 3 e 80 caracteres')
        return v

    @validator('data_nascimento')
    def validate_data_nascimento(cls, v):
        hoje = date.today()
        idade = relativedelta(hoje, v).years
        if idade < 5:
            raise ValueError('Aluno deve ter no mínimo 5 anos')
        return v

# API Routes
@app.get("/turmas")
def listar_turmas(db: Session = Depends(get_db)):
    turmas = db.query(models.Turma).all()
    return [turma.to_dict() for turma in turmas]

@app.post("/turmas")
def criar_turma(turma: TurmaBase, db: Session = Depends(get_db)):
    db_turma = models.Turma(**turma.dict())
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma.to_dict()

@app.get("/alunos")
def listar_alunos(
    search: Optional[str] = None,
    turma_id: Optional[int] = None,
    status: Optional[models.StatusEnum] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Aluno)
    
    if search:
        query = query.filter(models.Aluno.nome.ilike(f"%{search}%"))
    if turma_id:
        query = query.filter(models.Aluno.turma_id == turma_id)
    if status:
        query = query.filter(models.Aluno.status == status)
    
    alunos = query.all()
    return [aluno.to_dict() for aluno in alunos]

@app.post("/alunos")
def criar_aluno(aluno: AlunoBase, db: Session = Depends(get_db)):
    db_aluno = models.Aluno(**aluno.dict())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno.to_dict()

@app.put("/alunos/{aluno_id}")
def atualizar_aluno(aluno_id: int, aluno: AlunoBase, db: Session = Depends(get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    for key, value in aluno.dict().items():
        setattr(db_aluno, key, value)
    
    db.commit()
    db.refresh(db_aluno)
    return db_aluno.to_dict()

@app.delete("/alunos/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    db.delete(db_aluno)
    db.commit()
    return {"message": "Aluno deletado com sucesso"}

@app.post("/matriculas")
def matricular_aluno(aluno_id: int, turma_id: int, db: Session = Depends(get_db)):
    # Verificar se aluno existe
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Verificar se turma existe
    turma = db.query(models.Turma).filter(models.Turma.id == turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    # Verificar capacidade da turma
    alunos_na_turma = db.query(models.Aluno).filter(models.Aluno.turma_id == turma_id).count()
    if alunos_na_turma >= turma.capacidade:
        raise HTTPException(status_code=400, detail="Turma está cheia")
    
    # Atualizar aluno
    aluno.turma_id = turma_id
    aluno.status = models.StatusEnum.ATIVO
    
    db.commit()
    db.refresh(aluno)
    return aluno.to_dict()
