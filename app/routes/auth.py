from fastapi import APIRouter, Depends, HTTPException
from keycloak import KeycloakOpenID
from app.utils.authentication import get_user_profile, logout_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        logout_user(token)
        return {"message": "Logout successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile")
async def profile(token: str = Depends(oauth2_scheme)):
    try:
        user_profile = get_user_profile(token)
        return user_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
