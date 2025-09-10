# Relatório do Projeto - Sistema de Gestão Escolar

## 1. Introdução
Este relatório documenta o desenvolvimento do Sistema de Gestão Escolar, projeto realizado para a disciplina de Desenvolvimento Web. O sistema permite gerenciar alunos, turmas e matrículas de uma instituição de ensino.

## 2. Tecnologias Utilizadas

### Frontend
- **HTML5**: Estruturação semântica das páginas
- **CSS3**: Estilização com Flexbox e Grid Layout
- **JavaScript ES6+**: Interatividade e consumo da API REST

### Backend  
- **FastAPI**: Framework Python para criação da API REST
- **SQLAlchemy**: ORM para manipulação do banco de dados
- **SQLite**: Banco de dados relacional leve
- **Uvicorn**: Servidor ASGI para execução da aplicação

## 3. Arquitetura do Sistema

### Estrutura de Pastas
O projeto segue uma arquitetura separada entre frontend e backend:
- `/frontend`: Contém os arquivos estáticos (HTML, CSS, JS)
- `/backend`: Contém a API Python e configurações do banco

### Modelo de Dados
- **Turma**: id, nome, capacidade
- **Aluno**: id, nome, data_nascimento, email, status, turma_id

### API REST
Implementada seguindo padrões REST com retorno em JSON e códigos de status HTTP apropriados.

## 4. Funcionalidades Implementadas

### 4.1 Gestão de Alunos
- Listagem com filtros por turma, status e busca por nome
- Cadastro com validações de idade mínima (5 anos) e formato de email
- Edição e exclusão de registros
- Controle de status (ativo/inativo)

### 4.2 Gestão de Turmas
- Listagem de turmas com informações de capacidade e ocupação
- Cadastro de novas turmas

### 4.3 Sistema de Matrículas
- Matricula alunos em turmas respeitando limite de capacidade
- Alteração automática do status do aluno para "ativo"
- Validações de regras de negócio

### 4.4 Peculiaridades Implementadas
1. **Acessibilidade**: Atributos ARIA, foco visível, navegação por teclado
2. **Validações Customizadas**: Idade mínima de 5 anos, formato de email
3. **Filtros Avançados**: Busca em tempo real sem recarregamento da página

## 5. Identidade Visual
- Paleta de cores profissional (azul, verde, laranja)
- Tipografia legível (fonte Inter)
- Layout responsivo com duas colunas
- Componentes modais para formulários

## 6. Validações e Segurança
- Validações no frontend para melhor experiência do usuário
- Validações no backend para garantir integridade dos dados
- Sanitização de entradas para prevenir SQL injection
- Códigos de status HTTP apropriados para cada operação

## 7. Testes e Qualidade
- Dados de exemplo (seed) com 20+ registros para testes
- Tratamento de erros com mensagens informativas
- Feedback visual para ações do usuário

## 8. Conclusão
O projeto atendeu a todos os requisitos técnicos e funcionais especificados. A separação entre frontend e backend permite escalabilidade e manutenibilidade. A implementação das peculiaridades (acessibilidade, validações customizadas e filtros avançados) agregou valor significativo ao sistema.

## 9. Possíveis Melhorias Futuras
- Implementação de autenticação e autorização
- Relatórios mais avançados com gráficos
- Sistema de backup e restore do banco de dados
- Notificações por email para matrículas
- Versão mobile responsiva aprimorada
