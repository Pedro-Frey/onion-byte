# Onion Byte

Projeto backend de enriquecimento de leads e scoring com IA.

## Setup
1. Crie um ambiente virtual: `python -m venv venv`
2. Ative: `source venv/bin/activate`
3. Instale dependências: `pip install -r requirements.txt`
4. Configure as variáveis em `.env` baseando-se no `.env.example`
5. Rode o banco de dados e redis com `make docker-up` (necessita Docker)
6. Rode as migrações: `make migrate`
7. Inicie a API: `make dev`

A documentação da API ficará disponível em http://localhost:8000/docs
