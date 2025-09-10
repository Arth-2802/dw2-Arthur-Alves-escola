"""
Modelos de dados usando SQLAlchemy ORM
Define as tabelas Turma e Aluno com seus relacionamentos
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Turma(Base):
    """
    Modelo da tabela Turma
    Representa uma turma escolar com capacidade limitada
    """
    __tablename__ = "turmas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)  # Nome único da turma
    capacidade = Column(Integer, nullable=False)             # Máximo de alunos
    
    # Relacionamento com Aluno (um para muitos)
    # back_populates cria referência bidirecional
    alunos = relationship("Aluno", back_populates="turma")
    
    def __repr__(self):
        return f"<Turma(id={self.id}, nome='{self.nome}', capacidade={self.capacidade})>"

class Aluno(Base):
    """
    Modelo da tabela Aluno
    Representa um estudante com informações pessoais e status de matrícula
    """
    __tablename__ = "alunos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(80), nullable=False)                    # Nome obrigatório (3-80 chars)
    data_nascimento = Column(Date, nullable=False)              # Data de nascimento obrigatória
    email = Column(String(255), nullable=True, unique=True)     # Email único (opcional)
    status = Column(String(20), nullable=False, default="inativo")  # ativo/inativo
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=True)  # FK para turma (opcional)
    
    # Relacionamento com Turma (muitos para um)
    turma = relationship("Turma", back_populates="alunos")
    
    def __repr__(self):
        return f"<Aluno(id={self.id}, nome='{self.nome}', status='{self.status}')>"
    
    @property
    def idade(self):
        """
        Calcula a idade do aluno baseada na data de nascimento
        Retorna a idade em anos completos
        """
        hoje = datetime.date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
