from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import UUID
import os
from dotenv import load_dotenv
from ..config.db_config import get_db
from ..models.user_models import User
from ..schemas.auth_schemas import (
    UserCreate,
    UserLogin,
    TokenData,
    VerifyCodeRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from ..services.email_service import (
    generate_verification_code,
    send_verification_email,
    send_reset_password_email,
)
from ..config.db_config import get_db
from ..utils.hashing import hash_password, verify_password

load_dotenv()

# Secret Key & JWT Config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Register User
def register_user(user_data: UserCreate, background_tasks: BackgroundTasks, db: Session):
    existing_user = db.query(User).filter(User.email == user_data.email.strip().lower()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    new_user = User(
        name=user_data.name, 
        email=user_data.email.strip().lower(),
        hashed_password=hashed_password,
        created_at=datetime.utcnow(),
        is_verified=False,
        is_admin=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    verification_code = generate_verification_code()
    new_user.verification_token = verification_code
    db.commit()

    send_verification_email(new_user.email, verification_code, background_tasks)
    return new_user

# Verify Email
def verify_email(payload: VerifyCodeRequest, db: Session):
    user = db.query(User).filter(User.verification_token == payload.code).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    
    # Mark the user as verified
    user.is_verified = True
    user.verification_token = None
    db.commit()
    
    # Generate a token for the user after successful verification
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": str(user.id),
            "is_admin": user.is_admin
        }
    )
    
    return {
        "message": "Email successfully verified",
        "access_token": access_token,  
        "token_type": "bearer", 
        "user_id": str(user.id), 
        "email": user.email  
    }

# Login User
def login_user(user: UserLogin, db: Session):
    user_in_db = db.query(User).filter(User.email == user.email.strip().lower()).first()
    
    if not user_in_db or not verify_password(user.password, user_in_db.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not user_in_db.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified. Please verify your email before logging in.")

    access_token = create_access_token(
        data={
            "sub": user_in_db.email,
            "user_id": str(user_in_db.id),
            "is_admin": user_in_db.is_admin
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "name": user_in_db.name, 
        "user_id": str(user_in_db.id),
        "is_admin": user_in_db.is_admin
    }

# Forgot Password
def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session):
    user = db.query(User).filter(User.email == request.email.strip().lower()).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this email does not exist.")
    
    reset_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    user.reset_token = reset_token
    db.commit()

    send_reset_password_email(user.email, reset_token, background_tasks)
    return {"message": "Password reset link sent to your email."}

# Reset Password
def reset_password(request: ResetPasswordRequest, db: Session):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.hashed_password = hash_password(request.new_password)
    user.reset_token = None
    db.commit()
    return {"message": "Password reset successfully."}

# Get Current User
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id") 

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch the full User object from the database
        user = db.query(User).filter(User.id == UUID(user_id)).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user  
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Get Current Admin
def get_current_admin(current_user: TokenData = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

