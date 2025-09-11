"""
Script para criar usuário administrativo inicial
Execute este script após configurar o banco de dados
"""
from database import SessionLocal, engine
from models import Base, Usuario
from auth import criar_hash_senha
import datetime

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

def criar_usuario_admin():
    """
    Cria um usuário administrador inicial
    """
    db = SessionLocal()
    
    try:
        # Verifica se já existe um usuário admin
        admin_existente = db.query(Usuario).filter(Usuario.username == "admin").first()
        if admin_existente:
            print("Usuário admin já existe!")
            return
        
        # Cria o usuário admin
        senha_hash = criar_hash_senha("admin123")
        
        usuario_admin = Usuario(
            username="admin",
            email="admin@escola.com",
            senha_hash=senha_hash,
            nome_completo="Administrador do Sistema",
            ativo=True,
            data_criacao=datetime.datetime.utcnow()
        )
        
        db.add(usuario_admin)
        db.commit()
        
        print("Usuário administrador criado com sucesso!")
        print("Username: admin")
        print("Senha: admin123")
        print("IMPORTANTE: Altere a senha após o primeiro login!")
        
    except Exception as e:
        print(f"Erro ao criar usuário admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    criar_usuario_admin()
