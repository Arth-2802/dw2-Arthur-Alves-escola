from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    turma_id = Column(Integer, ForeignKey('turmas.id'))

    turma = relationship("Turma", back_populates="alunos")

class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    ano = Column(Integer)

    alunos = relationship("Aluno", back_populates="turma")