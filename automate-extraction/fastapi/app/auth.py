from datetime import datetime, timedelta
# from jose import JWTError, jwt
from jose.exceptions import JWTError
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv("FAST_API_SECRET_KEY")
ALGORITHM = os.getenv("FAST_API_ALGORITHM")

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt