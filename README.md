# Sistema de Vendas Online - Projeto Django

Este projeto foi desenvolvido como parte da disciplina de Desenvolvimento Web com Python, no curso de Análise e Desenvolvimento de Sistemas da Fatec Praia Grande.

## 🚀 Objetivo

Criar um sistema de vendas online que simula funcionalidades de um e-commerce, com autenticação de usuários, cadastro e listagem de produtos, consumo de APIs externas, e geração de relatórios.

## 🛠️ Requisitos

Para executar o projeto localmente, você precisará ter os seguintes softwares e extensões instalados:

### 🔧 Softwares
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [PostgreSQL](https://www.postgresql.org/) (se preferir, pode usar SQLite para testes)
- [Node.js](https://nodejs.org/) (caso precise compilar arquivos estáticos com ferramentas JS)

### 💼 Extensões VSCode recomendadas
- Python
- Django
- PostgreSQL
- .env Files

## ⚙️ Como rodar o projeto

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

Crie e ative um ambiente virtual:
python -m venv venv
e logo em seguida:
source venv/bin/activate  # No Windows: venv\Scripts\activate

Instale as dependências:
pip install -r requirements.txt
Configure o arquivo .env com suas variáveis (exemplo no .env.example).

Rode as migrações:
python manage.py migrate

Inicie o servidor:
python manage.py runserver
Acesse http://127.0.0.1:8000 no seu navegador. Pronto! 🚀
