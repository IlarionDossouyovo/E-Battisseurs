"""JWT Authentication for E-Battisseurs"""
from datetime import datetime, timedelta
from typing import Optional
import hashlib
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import os

# Security
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None


class User(BaseModel):
    id: str
    email: str
    name: str
    role: str = "user"
    is_active: bool = True


class UserInDB(User):
    password_hash: str


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.isoformat()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return TokenData(user_id=user_id, email=email)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from token"""
    token_data = decode_token(token)
    
    # Find user in database
    user_dict = None
    for email, user in USERS_DB.items():
        if user["id"] == token_data.user_id:
            user_dict = user
            break
    
    if user_dict is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return User(**user_dict)


# Mock users database
USERS_DB = {
    "admin@ebattisseurs.com": {
        "id": "user-001",
        "email": "admin@ebattisseurs.com",
        "name": "Admin",
        "role": "admin",
        "password_hash": hash_password("admin"),
        "is_active": True,
    },
    "user@ebattisseurs.com": {
        "id": "user-002",
        "email": "user@ebattisseurs.com",
        "name": "User",
        "role": "user",
        "password_hash": hash_password("user"),
        "is_active": True,
    },
}


def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    """Authenticate user"""
    user_dict = USERS_DB.get(email)
    if not user_dict:
        return None
    if not verify_password(password, user_dict["password_hash"]):
        return None
    return UserInDB(**user_dict)


# Auth router
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    """Login user"""
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=Token)
async def register(request: RegisterRequest):
    """Register new user"""
    if request.email in USERS_DB:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = f"user-{len(USERS_DB) + 1:03d}"
    password_hash = hash_password(request.password)
    
    USERS_DB[request.email] = {
        "id": user_id,
        "email": request.email,
        "name": request.name,
        "role": "user",
        "password_hash": password_hash,
        "is_active": True,
    }
    
    access_token = create_access_token(
        data={"sub": user_id, "email": request.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user"""
    return current_user