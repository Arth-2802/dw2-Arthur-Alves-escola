"""
Script de teste para verificar se a API está funcionando
"""
import requests
import json

def test_api():
    base_url = "http://localhost:8001"
    
    print("🧪 Testando API do Sistema de Gestão Escolar...")
    
    try:
        # Teste 1: Endpoint raiz
        print("\n1. Testando endpoint raiz...")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Resposta: {response.json()}")
        
        # Teste 2: Listar turmas
        print("\n2. Testando listagem de turmas...")
        response = requests.get(f"{base_url}/turmas")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            turmas = response.json()
            print(f"   Encontradas {len(turmas)} turmas")
            if turmas:
                print(f"   Primeira turma: {turmas[0]['nome']}")
        
        # Teste 3: Listar alunos
        print("\n3. Testando listagem de alunos...")
        response = requests.get(f"{base_url}/alunos")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            alunos = response.json()
            print(f"   Encontrados {len(alunos)} alunos")
            if alunos:
                print(f"   Primeiro aluno: {alunos[0]['nome']}")
        
        # Teste 4: Criar turma de teste
        print("\n4. Testando criação de turma...")
        nova_turma = {
            "nome": "Turma Teste API",
            "capacidade": 15
        }
        response = requests.post(f"{base_url}/turmas", json=nova_turma)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            turma_criada = response.json()
            print(f"   Turma criada: {turma_criada['nome']} (ID: {turma_criada['id']})")
        else:
            print(f"   Erro: {response.text}")
        
        print("\n✅ Testes concluídos!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API.")
        print("   Verifique se o servidor está executando em http://localhost:8001")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_api()
