from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, auth, utils, openai
from .database import engine, Base, get_db
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

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
    print("user from login endpoint: ", user)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.UserCreds = Depends(utils.get_current_user)):
    return current_user

@app.get("/fetch-all", response_model=List[dict])
def fetch_all(
    current_user: models.UserCreds = Depends(utils.get_current_user), 
    db: Session = Depends(get_db)):

    df = utils.fetch_data_as_dataframe(db)
    if isinstance(df, pd.DataFrame):
        return df.to_dict(orient='records')
    else:
        raise HTTPException(status_code=404, detail="No data found")

openai_client = openai.OpenAIClient(api_key=openai_api_key)

class OpenAiRequest(BaseModel):
    question: str
    context: str = None
    model: str = None


@app.post("/response-openai")
async def response_openai(request: OpenAiRequest, current_user: models.UserCreds = Depends(utils.get_current_user)):
    """
    API endpoint to handle questions and return responses from OpenAI.
    """
    try:
        response = openai_client.send_prompt(
            question=request.question,
            context=request.context,
            model=request.model
        )
        return {"question": request.question, "response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
class FetchContextRequest(BaseModel):
    question_id: str
    tool: str

@app.post("/fetch-context")
async def fetch_context(request: FetchContextRequest, 
                  db: Session = Depends(get_db), 
                  current_user: models.UserCreds = Depends(utils.get_current_user)):
    try:
        response = utils.fetch_context_from_s3(
            question_id=request.question_id,
            db=db,
            aws_profile="dev",
            tool=request.tool
        )
        return {"question_id": request.question_id, "context": response}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/fetch-steps")
async def fetch_steps(db: Session = Depends(get_db), 
                        question_id: str = None,
                        current_user: models.UserCreds = Depends(utils.get_current_user)):
    try:
        steps = utils.fetch_annotator_steps(db, question_id)
        return {"steps": steps}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))