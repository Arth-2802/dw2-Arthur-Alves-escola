# Sistema de Gestão Escolar

## Visão Geral
Este projeto é um mini sistema web para gestão escolar, desenvolvido para administrar alunos e turmas de forma eficiente. Possui um front-end em HTML5, CSS3 e JavaScript ES6, e um back-end com Python FastAPI, SQLite e SQLAlchemy.

## Estrutura do Projeto
O projeto está organizado em dois diretórios principais: `frontend` e `backend`.

```
school-management-system
├── backend
│   ├── app
│   │   ├── main.py          # Ponto de entrada da aplicação FastAPI
│   │   ├── models.py        # Modelos SQLAlchemy das entidades do banco
│   │   ├── schemas.py       # Schemas Pydantic para validação de dados
│   │   ├── database.py      # Conexão e gerenciamento da sessão do banco
│   │   ├── crud.py          # Operações CRUD para interação com o banco
│   │   └── routes.py        # Endpoints da API para gerenciamento das entidades
│   ├── requirements.txt      # Dependências do back-end
│   └── README.md             # Documentação do back-end
├── frontend
│   ├── index.html            # Documento HTML principal do front-end
│   ├── css
│   │   └── styles.css        # Estilos do front-end
│   ├── js
│   │   └── app.js            # Código JavaScript do front-end
│   └── README.md             # Documentação do front-end
└── README.md                 # Documentação geral do projeto
```

## Front-end
O front-end consiste em um documento HTML que fornece o layout do sistema de gestão escolar. Inclui:
- Cabeçalho com o título "Gestão Escolar"
- Barra de busca para filtrar alunos ou turmas
- Seções para exibir estatísticas e a listagem principal de alunos ou turmas

### Tecnologias Utilizadas
- HTML5
- CSS3
- JavaScript ES6

## Back-end
O back-end é construído com FastAPI e interage com um banco SQLite via SQLAlchemy. Disponibiliza endpoints REST para gerenciamento de alunos (Aluno) e turmas (Turma).

### Tecnologias Utilizadas
- Python
- FastAPI
- SQLite
- SQLAlchemy

## Instruções de Instalação

### Front-end
1. Navegue até o diretório `frontend`.
2. Abra o arquivo `index.html` em um navegador para visualizar a aplicação.

### Back-end
1. Navegue até o diretório `backend`.
2. Instale as dependências necessárias:
   ```
   pip install -r requirements.txt
   ```
3. Execute a aplicação FastAPI:
   ```
   uvicorn app.main:app --reload
   ```
4. Acesse a documentação da API em `http://127.0.0.1:8000/docs`.

## Informações Adicionais
Este projeto tem fins educacionais e pode ser expandido com funcionalidades extras, como autenticação de usuários, relatórios avançados e muito