from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, auth, utils
from .database import engine, Base, get_db
from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.UserCreds).filter(models.UserCreds.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    hashed_password = auth.hash_password(user.password)
    new_user = models.UserCreds(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.UserCreds).filter(models.UserCreds.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.UserCreds = Depends(utils.get_current_user)):
    return current_user