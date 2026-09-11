# Guia de Configuração e Desenvolvimento

Este guia descreve os passos necessários para configurar o ambiente de desenvolvimento do Onion Byte localmente.

## Pré-requisitos
- Python 3.11+
- Docker e Docker Compose
- Git

## Clone do repositório
```bash
git clone <url-do-repositorio> onion-byte
cd onion-byte
```

## Configuração do .env
Copie o arquivo de exemplo e ajuste as variáveis de ambiente:
```bash
cp .env.example .env
```
Edite o `.env` com suas chaves de API e configurações locais se necessário.

## Instalação de dependências
Crie um ambiente virtual (recomendado) e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` no Windows
make install
```

## Rodando com Docker
Para subir todos os serviços (PostgreSQL, Redis, API, Celery Worker) pelo Docker:
```bash
make docker-up
```

## Rodando localmente
Para rodar a aplicação localmente sem Docker (requer banco e redis rodando externamente):
```bash
make dev
```

## Executando testes
Para rodar os testes:
```bash
make test
```

## Executando migrações
Para aplicar as migrações no banco de dados:
```bash
make migrate
```
Para criar novas migrações após alterar os modelos:
```bash
make migrate-create
```
