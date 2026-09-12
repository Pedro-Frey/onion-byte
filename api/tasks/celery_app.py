from celery import Celery
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "onion_byte",
    broker=redis_url,
    backend=redis_url,
    include=["api.tasks.enrichment_task"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_always_eager=True,  # Força as tarefas a rodarem na hora (síncrono)
)
