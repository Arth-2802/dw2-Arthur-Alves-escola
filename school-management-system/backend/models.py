from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
import datetime

class StatusEnum(str, enum.Enum):
    ativo = "ativo"
    inativo = "inativo"

class Turma(Base):
    __tablename__ = "turmas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    capacidade = Column(Integer, nullable=False)
    alunos = relationship("Aluno", back_populates="turma")

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(80), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=True)
    turma = relationship("Turma", back_populates="alunos")
