from fastapi import FastAPI, HTTPException, status, Query, Response
from fastapi.responses import JSONResponse
import csv
from io import StringIO
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import datetime
import re

app = FastAPI(title="Sistema de Gestão Escolar")

Base.metadata.create_all(bind=engine)

# Utilitário para obter sessão do banco

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Validações
EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"

# Endpoints Turmas
@app.get("/turmas")
def listar_turmas(db: Session = next(get_db())):
    turmas = db.query(models.Turma).all()
    return turmas

@app.post("/turmas", status_code=201)
def criar_turma(turma: dict, db: Session = next(get_db())):
    nome = turma.get("nome")
    capacidade = turma.get("capacidade")
    if not nome or not isinstance(capacidade, int) or capacidade < 1:
        raise HTTPException(status_code=400, detail="Nome e capacidade válidos são obrigatórios.")
    nova_turma = models.Turma(nome=nome, capacidade=capacidade)
    db.add(nova_turma)
    db.commit()
    db.refresh(nova_turma)
    return nova_turma

# Endpoints Alunos
@app.get("/alunos")
def listar_alunos(search: str = Query(None), turma_id: int = Query(None), status: str = Query(None), format: str = Query("json"), db: Session = next(get_db())):
    query = db.query(models.Aluno)
    if search:
        query = query.filter(models.Aluno.nome.ilike(f"%{search}%"))
    if turma_id:
        query = query.filter(models.Aluno.turma_id == turma_id)
    if status:
        query = query.filter(models.Aluno.status == status)
    alunos = query.all()
    # Exportação CSV
    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "nome", "data_nascimento", "email", "status", "turma_id"])
        for a in alunos:
            writer.writerow([
                a.id,
                a.nome,
                a.data_nascimento.strftime("%Y-%m-%d"),
                a.email or "",
                a.status,
                a.turma_id or ""
            ])
        return Response(content=output.getvalue(), media_type="text/csv")
    # Exportação JSON padrão
    return [
        {
            "id": a.id,
            "nome": a.nome,
            "data_nascimento": a.data_nascimento.strftime("%Y-%m-%d"),
            "email": a.email,
            "status": a.status,
            "turma_id": a.turma_id
        } for a in alunos
    ]

@app.post("/alunos", status_code=201)
def criar_aluno(aluno: dict, db: Session = next(get_db())):
    nome = aluno.get("nome")
    data_nascimento = aluno.get("data_nascimento")
    email = aluno.get("email")
    status_ = aluno.get("status")
    turma_id = aluno.get("turma_id")
    # Validações
    if not nome or len(nome) < 3 or len(nome) > 80:
        raise HTTPException(status_code=400, detail="Nome deve ter entre 3 e 80 caracteres.")
    try:
        data_nasc = datetime.datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    except:
        raise HTTPException(status_code=400, detail="Data de nascimento inválida. Use o formato YYYY-MM-DD.")
    hoje = datetime.date.today()
    idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
    if data_nasc > hoje:
        raise HTTPException(status_code=400, detail="Data de nascimento não pode ser futura.")
    if idade < 5:
        raise HTTPException(status_code=400, detail="Aluno deve ter pelo menos 5 anos de idade.")
    if email and not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Email inválido.")
    if status_ not in ["ativo", "inativo"]:
        raise HTTPException(status_code=400, detail="Status deve ser 'ativo' ou 'inativo'.")
    novo_aluno = models.Aluno(nome=nome, data_nascimento=data_nasc, email=email, status=status_, turma_id=turma_id)
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno

@app.put("/alunos/{id}")
def atualizar_aluno(id: int, aluno: dict, db: Session = next(get_db())):
    obj = db.query(models.Aluno).filter(models.Aluno.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    nome = aluno.get("nome")
    data_nascimento = aluno.get("data_nascimento")
    email = aluno.get("email")
    status_ = aluno.get("status")
    turma_id = aluno.get("turma_id")
    if nome:
        if len(nome) < 3 or len(nome) > 80:
            raise HTTPException(status_code=400, detail="Nome deve ter entre 3 e 80 caracteres.")
        obj.nome = nome
    if data_nascimento:
        try:
            data_nasc = datetime.datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        except:
            raise HTTPException(status_code=400, detail="Data de nascimento inválida.")
        if data_nasc > datetime.date.today() or (datetime.date.today() - data_nasc).days < 5*365:
            raise HTTPException(status_code=400, detail="Aluno deve ter pelo menos 5 anos.")
        obj.data_nascimento = data_nasc
    if email:
        if not re.match(EMAIL_REGEX, email):
            raise HTTPException(status_code=400, detail="Email inválido.")
        obj.email = email
    if status_:
        if status_ not in ["ativo", "inativo"]:
            raise HTTPException(status_code=400, detail="Status deve ser 'ativo' ou 'inativo'.")
        obj.status = status_
    obj.turma_id = turma_id
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/alunos/{id}")
def excluir_aluno(id: int, db: Session = next(get_db())):
    obj = db.query(models.Aluno).filter(models.Aluno.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    db.delete(obj)
    db.commit()
    return JSONResponse(content={"detail": "Aluno excluído com sucesso."}, status_code=200)

# Matrícula
@app.post("/matriculas", status_code=201)
def matricular_aluno(body: dict, db: Session = next(get_db())):
    aluno_id = body.get("aluno_id")
    turma_id = body.get("turma_id")
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    turma = db.query(models.Turma).filter(models.Turma.id == turma_id).first()
    if not aluno or not turma:
        raise HTTPException(status_code=404, detail="Aluno ou turma não encontrados.")
    ocupacao = db.query(models.Aluno).filter(models.Aluno.turma_id == turma_id).count()
    if ocupacao >= turma.capacidade:
        raise HTTPException(status_code=400, detail="Capacidade da turma atingida.")
    aluno.status = "ativo"
    aluno.turma_id = turma_id
    db.commit()
    db.refresh(aluno)
    return aluno
