from database import SessionLocal, engine, Base
import models
import datetime

Base.metadata.create_all(bind=engine)
db = SessionLocal()

turmas = [
    models.Turma(nome="Turma A", capacidade=10),
    models.Turma(nome="Turma B", capacidade=8),
    models.Turma(nome="Turma C", capacidade=12),
    models.Turma(nome="Turma D", capacidade=6)
]
for t in turmas:
    db.add(t)
db.commit()

turma_ids = [t.id for t in db.query(models.Turma).all()]

alunos = [
    models.Aluno(nome="Ana Silva", data_nascimento=datetime.date(2010,5,10), email="ana@email.com", status="ativo", turma_id=turma_ids[0]),
    models.Aluno(nome="Bruno Souza", data_nascimento=datetime.date(2011,7,22), email="bruno@email.com", status="ativo", turma_id=turma_ids[1]),
    models.Aluno(nome="Carlos Lima", data_nascimento=datetime.date(2012,3,15), email="carlos@email.com", status="inativo", turma_id=None),
    models.Aluno(nome="Daniela Costa", data_nascimento=datetime.date(2013,8,30), email="daniela@email.com", status="ativo", turma_id=turma_ids[2]),
    models.Aluno(nome="Eduardo Alves", data_nascimento=datetime.date(2010,12,5), email="eduardo@email.com", status="ativo", turma_id=turma_ids[0]),
    models.Aluno(nome="Fernanda Dias", data_nascimento=datetime.date(2011,2,18), email="fernanda@email.com", status="inativo", turma_id=None),
    models.Aluno(nome="Gabriel Martins", data_nascimento=datetime.date(2012,11,9), email="gabriel@email.com", status="ativo", turma_id=turma_ids[1]),
    models.Aluno(nome="Helena Rocha", data_nascimento=datetime.date(2013,6,25), email="helena@email.com", status="ativo", turma_id=turma_ids[2]),
    models.Aluno(nome="Igor Pereira", data_nascimento=datetime.date(2010,9,14), email="igor@email.com", status="ativo", turma_id=turma_ids[0]),
    models.Aluno(nome="Juliana Melo", data_nascimento=datetime.date(2011,4,3), email="juliana@email.com", status="inativo", turma_id=None),
    models.Aluno(nome="Karla Nunes", data_nascimento=datetime.date(2012,1,27), email="karla@email.com", status="ativo", turma_id=turma_ids[1]),
    models.Aluno(nome="Lucas Freitas", data_nascimento=datetime.date(2013,10,19), email="lucas@email.com", status="ativo", turma_id=turma_ids[2]),
    models.Aluno(nome="Marina Teixeira", data_nascimento=datetime.date(2010,6,8), email="marina@email.com", status="ativo", turma_id=turma_ids[0]),
    models.Aluno(nome="Nicolas Barros", data_nascimento=datetime.date(2011,12,12), email="nicolas@email.com", status="inativo", turma_id=None),
    models.Aluno(nome="Olivia Castro", data_nascimento=datetime.date(2012,8,2), email="olivia@email.com", status="ativo", turma_id=turma_ids[1])
]
for a in alunos:
    db.add(a)
db.commit()
db.close()
