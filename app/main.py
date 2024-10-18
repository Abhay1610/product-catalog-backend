from fastapi import FastAPI, Depends, HTTPException, Body, Request
from sqlalchemy.orm import Session
from keycloak import KeycloakOpenID
from .database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.tasks.tasks import add_to_catalog
from app.routes.auth import router as auth_router
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.utils.authentication import authenticate_user, introspect_token, get_user_profile, logout_user
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as necessary
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/",
    client_id="my-app",
    realm_name="my-realm"
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@app.post("/auth/login")
async def login(username: str = Body(...), password: str = Body(...)):
    try:
        access_token = authenticate_user(username, password)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")
    
    try:
        token_response = keycloak_openid.token(code=code)
        access_token = token_response.get("access_token")
        refresh_token = token_response.get("refresh_token")

        user_info = get_user_profile(access_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_info": user_info
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Create a product
@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    add_to_catalog.delay(new_product.id)

    return new_product

@app.get("/products/protected/", response_model=list[ProductResponse])
def get_products(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("Accessing protected products endpoint")  
    try:
        # Call introspect_token to validate the token
        introspect_data = introspect_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    print("Introspection Data:", introspect_data)

    return db.query(Product).all()

# Include the authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
