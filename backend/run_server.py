"""
Script para executar o servidor da API
"""
import os
import sys

# Adicionar o diretório atual ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from app import app

if __name__ == "__main__":
    print("🚀 Iniciando Sistema de Gestão Escolar...")
    print("📍 API: http://localhost:8001")
    print("📖 Documentação: http://localhost:8001/docs")
    print("📁 Frontend: Abra o arquivo frontend/index.html no navegador")
    print("\n⚡ Servidor executando...")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8001,
        log_level="info"
    )
