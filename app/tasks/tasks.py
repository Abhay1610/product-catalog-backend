from app.celery_app import celery_app
from app.models.product import Product
from app.database import SessionLocal

@celery_app.task
def add_to_catalog(product_data: dict):
    db = SessionLocal()
    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    db.close()
