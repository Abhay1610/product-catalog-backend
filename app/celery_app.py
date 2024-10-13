from celery import Celery

celery_app = Celery(
    "catalog",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
# Set additional configuration options
celery_app.conf.broker_connection_retry_on_startup = True