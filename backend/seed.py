# seed.py - Popular banco com dados iniciais
from database import SessionLocal
from models import Aluno, Turma
from datetime import date, timedelta
import random

def seed():
    db = SessionLocal()
    turmas = [
        Turma(nome=f"Turma {i+1}", capacidade=random.randint(20, 35)) for i in range(4)
    ]
    db.add_all(turmas)
    db.commit()
    alunos = []
    for i in range(20):
        turma = random.choice(turmas)
        aluno = Aluno(
            nome=f"Aluno {i+1}",
            data_nascimento=date.today() - timedelta(days=365*random.randint(6, 18)),
            email=f"aluno{i+1}@escola.com",
            status=random.choice(["ativo", "inativo"]),
            turma_id=turma.id
        )
        alunos.append(aluno)
    db.add_all(alunos)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
