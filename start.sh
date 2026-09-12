#!/bin/bash
# Executa as migrações do banco de dados
python -m alembic upgrade head

# Inicia o Celery em background para rodar os crawlers
celery -A api.tasks.celery_app worker --loglevel=info &

# Inicia o servidor da API em foreground
uvicorn api.main:app --host 0.0.0.0 --port $PORT
