from app.celery_app import celery_app
from app.models.product import Product
from app.schemas.product import ProductCreate
from sqlalchemy.orm import Session
from app.database import get_db

# Celery task with retry logic
@celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 10})
def add_to_catalog(product_data: dict):
    db = next(get_db())
    try:
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
    except Exception as e:
        db.rollback()  # Rollback transaction on error
        raise e
    finally:
        db.close()
