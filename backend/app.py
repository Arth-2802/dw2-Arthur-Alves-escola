# app.py - FastAPI principal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Aluno, Turma
from database import engine, Base

app = FastAPI(title="Gestão Escolar API")

# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# Endpoints virão aqui...
