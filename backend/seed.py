"""
Script para popular o banco de dados com dados de exemplo
Cria turmas e alunos para demonstração e testes
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Turma, Aluno
import datetime

# Recria as tabelas
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def criar_dados_exemplo():
    """
    Cria dados de exemplo no banco:
    - 5 turmas com diferentes capacidades
    - 25 alunos distribuídos entre as turmas
    """
    db = SessionLocal()
    
    try:
        # === CRIANDO TURMAS ===
        turmas_dados = [
            {"nome": "1º Ano A - Manhã", "capacidade": 25},
            {"nome": "1º Ano B - Tarde", "capacidade": 25},
            {"nome": "2º Ano A - Manhã", "capacidade": 30},
            {"nome": "3º Ano A - Manhã", "capacidade": 20},
            {"nome": "3º Ano B - Tarde", "capacidade": 20},
        ]
        
        turmas = []
        for turma_data in turmas_dados:
            turma = Turma(**turma_data)
            db.add(turma)
            turmas.append(turma)
        
        db.commit()
        print(f"✅ Criadas {len(turmas)} turmas")
        
        # === CRIANDO ALUNOS ===
        alunos_dados = [
            # 1º Ano A - Manhã (5 alunos)
            {"nome": "Ana Silva Santos", "data_nascimento": datetime.date(2017, 3, 15), "email": "ana.silva@email.com", "status": "ativo", "turma_id": 1},
            {"nome": "Bruno Oliveira Costa", "data_nascimento": datetime.date(2017, 7, 22), "email": "bruno.oliveira@email.com", "status": "ativo", "turma_id": 1},
            {"nome": "Carla Mendes Lima", "data_nascimento": datetime.date(2017, 1, 8), "email": "carla.mendes@email.com", "status": "ativo", "turma_id": 1},
            {"nome": "Diego Ferreira Rocha", "data_nascimento": datetime.date(2017, 9, 12), "email": "diego.ferreira@email.com", "status": "ativo", "turma_id": 1},
            {"nome": "Eduarda Alves Pereira", "data_nascimento": datetime.date(2017, 5, 30), "email": "eduarda.alves@email.com", "status": "ativo", "turma_id": 1},
            
            # 1º Ano B - Tarde (5 alunos)
            {"nome": "Felipe Santos Barbosa", "data_nascimento": datetime.date(2017, 4, 18), "email": "felipe.santos@email.com", "status": "ativo", "turma_id": 2},
            {"nome": "Gabriela Costa Martins", "data_nascimento": datetime.date(2017, 11, 25), "email": "gabriela.costa@email.com", "status": "ativo", "turma_id": 2},
            {"nome": "Henrique Lima Souza", "data_nascimento": datetime.date(2017, 2, 14), "email": "henrique.lima@email.com", "status": "ativo", "turma_id": 2},
            {"nome": "Isabela Rocha Fernandes", "data_nascimento": datetime.date(2017, 8, 7), "email": "isabela.rocha@email.com", "status": "ativo", "turma_id": 2},
            {"nome": "João Pedro Silva", "data_nascimento": datetime.date(2017, 6, 19), "email": "joao.pedro@email.com", "status": "ativo", "turma_id": 2},
            
            # 2º Ano A - Manhã (6 alunos)
            {"nome": "Laura Oliveira Santos", "data_nascimento": datetime.date(2016, 3, 10), "email": "laura.oliveira@email.com", "status": "ativo", "turma_id": 3},
            {"nome": "Mateus Costa Alves", "data_nascimento": datetime.date(2016, 7, 28), "email": "mateus.costa@email.com", "status": "ativo", "turma_id": 3},
            {"nome": "Natália Lima Pereira", "data_nascimento": datetime.date(2016, 1, 16), "email": "natalia.lima@email.com", "status": "ativo", "turma_id": 3},
            {"nome": "Otávio Mendes Rocha", "data_nascimento": datetime.date(2016, 9, 3), "email": "otavio.mendes@email.com", "status": "ativo", "turma_id": 3},
            {"nome": "Priscila Santos Costa", "data_nascimento": datetime.date(2016, 5, 21), "email": "priscila.santos@email.com", "status": "ativo", "turma_id": 3},
            {"nome": "Rafael Alves Lima", "data_nascimento": datetime.date(2016, 12, 5), "email": "rafael.alves@email.com", "status": "ativo", "turma_id": 3},
            
            # 3º Ano A - Manhã (5 alunos)
            {"nome": "Sofia Ferreira Barbosa", "data_nascimento": datetime.date(2015, 4, 12), "email": "sofia.ferreira@email.com", "status": "ativo", "turma_id": 4},
            {"nome": "Thiago Costa Martins", "data_nascimento": datetime.date(2015, 8, 27), "email": "thiago.costa@email.com", "status": "ativo", "turma_id": 4},
            {"nome": "Vitória Lima Souza", "data_nascimento": datetime.date(2015, 2, 9), "email": "vitoria.lima@email.com", "status": "ativo", "turma_id": 4},
            {"nome": "Wagner Rocha Silva", "data_nascimento": datetime.date(2015, 10, 15), "email": "wagner.rocha@email.com", "status": "ativo", "turma_id": 4},
            {"nome": "Yasmin Santos Pereira", "data_nascimento": datetime.date(2015, 6, 23), "email": "yasmin.santos@email.com", "status": "ativo", "turma_id": 4},
            
            # 3º Ano B - Tarde (4 alunos ativos + 1 inativo)
            {"nome": "Arthur Oliveira Costa", "data_nascimento": datetime.date(2015, 3, 18), "email": "arthur.oliveira@email.com", "status": "ativo", "turma_id": 5},
            {"nome": "Beatriz Mendes Lima", "data_nascimento": datetime.date(2015, 7, 11), "email": "beatriz.mendes@email.com", "status": "ativo", "turma_id": 5},
            {"nome": "Carlos Alves Rocha", "data_nascimento": datetime.date(2015, 11, 4), "email": "carlos.alves@email.com", "status": "ativo", "turma_id": 5},
            {"nome": "Daniela Santos Barbosa", "data_nascimento": datetime.date(2015, 5, 29), "email": "daniela.santos@email.com", "status": "ativo", "turma_id": 5},
            {"nome": "Eduardo Costa Martins", "data_nascimento": datetime.date(2015, 9, 17), "email": "eduardo.costa@email.com", "status": "inativo", "turma_id": 5},
            
            # Alunos sem turma (para demonstrar filtros)
            {"nome": "Fernanda Lima Souza", "data_nascimento": datetime.date(2016, 4, 6), "email": "fernanda.lima@email.com", "status": "inativo", "turma_id": None},
            {"nome": "Gustavo Rocha Silva", "data_nascimento": datetime.date(2017, 10, 13), "email": "gustavo.rocha@email.com", "status": "inativo", "turma_id": None},
        ]
        
        for aluno_data in alunos_dados:
            aluno = Aluno(**aluno_data)
            db.add(aluno)
        
        db.commit()
        print(f"✅ Criados {len(alunos_dados)} alunos")
        
        # === ESTATÍSTICAS ===
        total_turmas = db.query(Turma).count()
        total_alunos = db.query(Aluno).count()
        alunos_ativos = db.query(Aluno).filter(Aluno.status == "ativo").count()
        alunos_matriculados = db.query(Aluno).filter(Aluno.turma_id.isnot(None)).count()
        
        print("\n📊 ESTATÍSTICAS DO BANCO:")
        print(f"   • Total de turmas: {total_turmas}")
        print(f"   • Total de alunos: {total_alunos}")
        print(f"   • Alunos ativos: {alunos_ativos}")
        print(f"   • Alunos matriculados: {alunos_matriculados}")
        
        print("\n🎓 OCUPAÇÃO POR TURMA:")
        for turma in db.query(Turma).all():
            ocupacao = db.query(Aluno).filter(
                Aluno.turma_id == turma.id,
                Aluno.status == "ativo"
            ).count()
            print(f"   • {turma.nome}: {ocupacao}/{turma.capacidade} alunos")
        
        print(f"\n✅ Banco de dados populado com sucesso!")
        print(f"📁 Arquivo: backend/app.db")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    criar_dados_exemplo()
