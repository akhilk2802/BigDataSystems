from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    username: str
    email: EmailStr
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class GaiaDataset(BaseModel):
    task_id: str
    question: str
    level: int
    final_answer: str
    file_name: str
    file_path: str
    annotator_metadata: str
    split_type: str
    s3_url: str
    file_extension: str
    s3_url_extracted_azure: str
    s3_url_extracted_pypdf: str

    class Config:
        orm_mode: True