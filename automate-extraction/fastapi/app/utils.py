from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from sqlalchemy import text
import boto3
import json
from .models import UserCreds
from .auth import SECRET_KEY, ALGORITHM
import pandas as pd
from urllib.parse import urlparse



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(UserCreds).filter(UserCreds.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def fetch_data_as_dataframe(db: Session):
    query = "SELECT * FROM assignment2.gaia_dataset_tbl"
    result = db.execute(query)
    data = [dict(row) for row in result]
    df = pd.DataFrame(data)
    df.fillna('', inplace=True)
    return df

def fetch_annotator_steps(db: Session, question_id: str):
    query = text(f"SELECT Annotator Metadata FROM assignment2.gaia_dataset_tbl WHERE task_id = :task_id")
    result = db.execute(query, {'task_id': question_id}).fetchone()
    if result is None:
        raise ValueError(f"No entry found for question_id {question_id}")
    return json.loads(result[0])

    

def fetch_context_from_s3(question_id: str, db: Session, aws_profile: str, tool: str):
    
    if tool == "azure":
        column_name = "s3_url_extracted_azure"
    elif tool == "pypdf":
        column_name = "s3_url_extracted_pypdf"
    else:
        raise ValueError(f"Unsupported tool: {tool}")

    
    query = text(f"SELECT {column_name} FROM assignment2.gaia_dataset_tbl WHERE task_id = :task_id")
    result = db.execute(query, {'task_id': question_id}).fetchone()

    if result is None:
        raise ValueError(f"No entry found for question_id {question_id}")

    s3_url = result[column_name]

    if not s3_url:
        raise ValueError(f"No URL found in column {column_name} for question_id {question_id}")

    
    parsed_url = urlparse(s3_url)
    if parsed_url.scheme != 'https':
        raise ValueError(f"Invalid URL scheme: {parsed_url.scheme}")

    # Extract bucket name and object key from the URL
    bucket_name = parsed_url.netloc.split('.')[0]
    object_key = parsed_url.path.lstrip('/')

    # Initialize a Boto3 session with the specified profile
    session = boto3.Session(profile_name=aws_profile)
    s3_client = session.client('s3')

    try:
        # Retrieve the JSON object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')
        json_content = json.loads(content)
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve or parse JSON from S3: {e}")

    return json_content

    