from sqlalchemy.orm import Session
from . import models, schemas

def create_aluno(db: Session, aluno: schemas.AlunoCreate):
    db_aluno = models.Aluno(**aluno.dict())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def get_aluno(db: Session, aluno_id: int):
    return db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()

def get_alunos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Aluno).offset(skip).limit(limit).all()

def update_aluno(db: Session, aluno_id: int, aluno: schemas.AlunoUpdate):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if db_aluno:
        for key, value in aluno.dict(exclude_unset=True).items():
            setattr(db_aluno, key, value)
        db.commit()
        db.refresh(db_aluno)
    return db_aluno

def delete_aluno(db: Session, aluno_id: int):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if db_aluno:
        db.delete(db_aluno)
        db.commit()
    return db_aluno

def create_turma(db: Session, turma: schemas.TurmaCreate):
    db_turma = models.Turma(**turma.dict())
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma

def get_turma(db: Session, turma_id: int):
    return db.query(models.Turma).filter(models.Turma.id == turma_id).first()

def get_turmas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Turma).offset(skip).limit(limit).all()

def update_turma(db: Session, turma_id: int, turma: schemas.TurmaUpdate):
    db_turma = db.query(models.Turma).filter(models.Turma.id == turma_id).first()
    if db_turma:
        for key, value in turma.dict(exclude_unset=True).items():
            setattr(db_turma, key, value)
        db.commit()
        db.refresh(db_turma)
    return db_turma

def delete_turma(db: Session, turma_id: int):
    db_turma = db.query(models.Turma).filter(models.Turma.id == turma_id).first()
    if db_turma:
        db.delete(db_turma)
        db.commit()
    return db_turma