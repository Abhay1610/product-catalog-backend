from celery import Celery

celery_app = Celery(
    "catalog",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Set additional configuration options
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Only accept JSON tasks
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True
)
