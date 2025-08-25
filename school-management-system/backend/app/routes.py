from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import get_db

router = APIRouter()

@router.post("/alunos/", response_model=schemas.Aluno)
def create_aluno(aluno: schemas.AlunoCreate, db: Session = next(get_db())):
    db_aluno = crud.get_aluno_by_email(db, email=aluno.email)
    if db_aluno:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_aluno(db=db, aluno=aluno)

@router.get("/alunos/", response_model=list[schemas.Aluno])
def read_alunos(skip: int = 0, limit: int = 10, db: Session = next(get_db())):
    alunos = crud.get_alunos(db, skip=skip, limit=limit)
    return alunos

@router.get("/alunos/{aluno_id}", response_model=schemas.Aluno)
def read_aluno(aluno_id: int, db: Session = next(get_db())):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno not found")
    return db_aluno

@router.put("/alunos/{aluno_id}", response_model=schemas.Aluno)
def update_aluno(aluno_id: int, aluno: schemas.AlunoUpdate, db: Session = next(get_db())):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno not found")
    return crud.update_aluno(db=db, aluno_id=aluno_id, aluno=aluno)

@router.delete("/alunos/{aluno_id}", response_model=schemas.Aluno)
def delete_aluno(aluno_id: int, db: Session = next(get_db())):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno not found")
    return crud.delete_aluno(db=db, aluno_id=aluno_id)

@router.post("/turmas/", response_model=schemas.Turma)
def create_turma(turma: schemas.TurmaCreate, db: Session = next(get_db())):
    return crud.create_turma(db=db, turma=turma)

@router.get("/turmas/", response_model=list[schemas.Turma])
def read_turmas(skip: int = 0, limit: int = 10, db: Session = next(get_db())):
    turmas = crud.get_turmas(db, skip=skip, limit=limit)
    return turmas

@router.get("/turmas/{turma_id}", response_model=schemas.Turma)
def read_turma(turma_id: int, db: Session = next(get_db())):
    db_turma = crud.get_turma(db, turma_id=turma_id)
    if db_turma is None:
        raise HTTPException(status_code=404, detail="Turma not found")
    return db_turma

@router.put("/turmas/{turma_id}", response_model=schemas.Turma)
def update_turma(turma_id: int, turma: schemas.TurmaUpdate, db: Session = next(get_db())):
    db_turma = crud.get_turma(db, turma_id=turma_id)
    if db_turma is None:
        raise HTTPException(status_code=404, detail="Turma not found")
    return crud.update_turma(db=db, turma_id=turma_id, turma=turma)

@router.delete("/turmas/{turma_id}", response_model=schemas.Turma)
def delete_turma(turma_id: int, db: Session = next(get_db())):
    db_turma = crud.get_turma(db, turma_id=turma_id)
    if db_turma is None:
        raise HTTPException(status_code=404, detail="Turma not found")
    return crud.delete_turma(db=db, turma_id=turma_id)