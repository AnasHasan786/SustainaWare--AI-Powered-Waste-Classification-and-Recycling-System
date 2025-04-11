from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from PIL import Image
from ..config.db_config import get_db
from ..schemas.auth_schemas import (
    UserCreate, UserLogin, UserResponse, GoogleAuthRequest, VerifyCodeRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from ..services.auth_service import (
    register_user, verify_email, login_user, forgot_password, reset_password, create_access_token, get_current_user
)
from ..models.user_models import User
from dotenv import load_dotenv
import os
import shutil
import uuid

# Load environment variables
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

if not GOOGLE_CLIENT_ID:
    raise ValueError("GOOGLE_CLIENT_ID is not set in the .env file")

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Register a new user with the given information and return a JWT token.
    """
    new_user = register_user(user, background_tasks, db)

    token = create_access_token(
        data={"user_id": str(new_user.id), "email": new_user.email, "name": new_user.name}
    )

    return {
        "success": True,
        "message": "User registered successfully",
        "token": token, 
        "user": {
            "id": str(new_user.id),
            "name": new_user.name,
            "email": new_user.email,
            "is_verified": new_user.is_verified
        }
    }


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT token.
    """
    token = login_user(user, db)  

    return {
        "success": True,
        "message": "Login successful",
        "token": token["access_token"],  
        "user": {
            "name": token["name"],  
            "user_id": token["user_id"],
            "is_admin": token["is_admin"]
        }
    }

@router.post("/google-login", status_code=status.HTTP_200_OK)
async def google_login(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    """
    Authenticate user using Google OAuth and return a JWT token.
    """
    try:
        idinfo = id_token.verify_oauth2_token(payload.token, requests.Request())
        if idinfo["aud"] != GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token: Client ID mismatch")
        
        email = idinfo["email"]
        name = idinfo.get("name", "Google User")
        avatar = idinfo.get("picture", "")
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(name=name, email=email, avatar=avatar, is_verified=True)
            db.add(user)
            db.commit()
            db.refresh(user)
        
        jwt_token = create_access_token({"user_id": str(user.id), "email": user.email, "name": user.name})
        
        return {
            "success": True,
            "message": "Google login successful",
            "token": jwt_token,
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "avatar": user.avatar,
                "is_verified": user.is_verified
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token: " + str(e))

@router.post("/verify-email")
async def verify_email_endpoint(
    payload: VerifyCodeRequest, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    try:
        # Call the verify_email function and return the response
        response = verify_email(payload, db)
        return response
    except HTTPException as e:
        # Catch any HTTPException and return the error details
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password_endpoint(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Initiate the password reset process by sending a reset email.
    """
    result = forgot_password(request, background_tasks, db)
    return {"success": True, "message": "Password reset email sent", "data": result}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password_endpoint(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset the user's password with the given information.
    """
    result = reset_password(request, db)
    return {"success": True, "message": "Password reset successful", "data": result}

@router.get("/me", response_model=UserResponse)
def get_user_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user

