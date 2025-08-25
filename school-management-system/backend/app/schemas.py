from pydantic import BaseModel
from typing import List, Optional

class Aluno(BaseModel):
    id: Optional[int] = None
    nome: str
    idade: int
    turma_id: int

class Turma(BaseModel):
    id: Optional[int] = None
    nome: str
    ano: int
    alunos: List[Aluno] = []