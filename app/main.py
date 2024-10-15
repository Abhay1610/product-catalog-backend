from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from keycloak import KeycloakOpenID
from .database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.tasks.tasks import add_to_catalog
from app.routes.auth import router as auth_router  # Import the new auth router
from app.utils.authentication import authenticate_user

app = FastAPI()

# Initialize Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/auth/",
    client_id="my-app",  # Replace with your Keycloak client ID
    realm_name="my-realm"  # Replace with your Keycloak realm
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a product (with database commit and then Celery task)
@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Create a new product instance
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price
    )
    
    # Add to the database and commit
    db.add(new_product)
    db.commit()
    db.refresh(new_product)  # Refresh to get the generated ID
    
    # Trigger the Celery task to perform any additional background work
    add_to_catalog.delay(new_product.id)

    # Return the newly created product
    return new_product

# Get a product by ID (no authentication required)
@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Protected route to list all products (requires Keycloak authentication)
@app.get("/products/protected/", response_model=list[ProductResponse])
def get_products(username: str, password: str, db: Session = Depends(get_db)):
    # Authenticate user and get token
    access_token = authenticate_user(username, password)
    
    # Here, you can add any further token validation if needed
    return db.query(Product).all()

# Include the authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
