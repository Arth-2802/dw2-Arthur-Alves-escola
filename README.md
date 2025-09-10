# Sistema de Gestão Escolar

## Descrição
Sistema de gestão de turmas e matrículas escolares desenvolvido como projeto acadêmico.

## Tecnologias Utilizadas
- **Frontend**: HTML5, CSS3 (Flexbox/Grid), JavaScript ES6+
- **Backend**: FastAPI (Python)
- **Banco de Dados**: SQLite com SQLAlchemy
- **Arquitetura**: REST API com JSON

## Estrutura do Projeto
```
/frontend
  index.html          # Página principal
  styles.css          # Estilos e identidade visual
  scripts.js          # Lógica de interação e CRUD
/backend
  app.py              # Servidor FastAPI e rotas
  models.py           # Modelos SQLAlchemy
  database.py         # Configuração do banco
  seed.py             # Dados iniciais
  requirements.txt    # Dependências Python
  app.db              # Banco SQLite (gerado automaticamente)
```

## Identidade Visual
- **Primária**: #2563EB (azul)
- **Secundária**: #10B981 (verde) 
- **Acento**: #F97316 (laranja)
- **Fundo**: #F1F5F9 (cinza claro)
- **Texto**: #0B1220
- **Fonte**: Inter

## Funcionalidades
- ✅ CRUD de Alunos com validações
- ✅ CRUD de Turmas 
- ✅ Sistema de Matrículas com controle de capacidade
- ✅ Filtros avançados (turma, status, busca por nome)
- ✅ Acessibilidade (ARIA, foco, tabindex)
- ✅ Validações customizadas (idade mínima 5 anos)
- ✅ Interface responsiva

## Como Executar

### Backend
1. Navegue até a pasta backend:
   ```bash
   cd backend
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o servidor:
   ```bash
   python app.py
   ```

### Frontend
1. Abra o arquivo `frontend/index.html` no navegador
2. Ou use um servidor local:
   ```bash
   cd frontend
   python -m http.server 8080
   ```

## API Endpoints
- `GET /alunos` - Lista alunos com filtros opcionais
- `POST /alunos` - Cria novo aluno
- `PUT /alunos/{id}` - Atualiza aluno
- `DELETE /alunos/{id}` - Remove aluno
- `GET /turmas` - Lista turmas
- `POST /turmas` - Cria nova turma
- `POST /matriculas` - Matricula aluno em turma

## Autor
Arthur Alves - Projeto de Desenvolvimento Web
