from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class StatusEnum(str, enum.Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"

class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(80), nullable=False)
    capacidade = Column(Integer, nullable=False)
    
    # Relationship
    alunos = relationship("Aluno", back_populates="turma")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "capacidade": self.capacidade,
            "ocupacao": len(self.alunos)
        }

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(80), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String(120), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.INATIVO)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=True)

    # Relationship
    turma = relationship("Turma", back_populates="alunos")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento.isoformat(),
            "email": self.email,
            "status": self.status,
            "turma_id": self.turma_id
        }
