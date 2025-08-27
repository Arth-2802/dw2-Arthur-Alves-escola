from datetime import date
from database import engine, SessionLocal
import models

def create_sample_data():
    db = SessionLocal()
    
    # Criar turmas
    turmas = [
        models.Turma(nome="1º Ano A", capacidade=30),
        models.Turma(nome="2º Ano A", capacidade=25),
        models.Turma(nome="3º Ano A", capacidade=20)
    ]
    
    for turma in turmas:
        db.add(turma)
    
    db.commit()
    
    # Criar alunos
    alunos = [
        models.Aluno(
            nome="João Silva",
            data_nascimento=date(2015, 5, 15),
            email="joao@email.com",
            status=models.StatusEnum.ATIVO,
            turma_id=1
        ),
        models.Aluno(
            nome="Maria Santos",
            data_nascimento=date(2014, 8, 20),
            email="maria@email.com",
            status=models.StatusEnum.ATIVO,
            turma_id=2
        ),
        models.Aluno(
            nome="Pedro Oliveira",
            data_nascimento=date(2013, 3, 10),
            status=models.StatusEnum.INATIVO
        )
    ]
    
    for aluno in alunos:
        db.add(aluno)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Create sample data
    create_sample_data()
