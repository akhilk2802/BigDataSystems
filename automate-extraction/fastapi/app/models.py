from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class UserCreds(Base):
    __tablename__ = "user_creds"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    is_active = Column(Boolean, default=True)


# class GaiaDataset(Base):
#     __tablename__ = "gaia_dataset_tbl"
#     __table_args__ = {'schema': 'assignment2'}
#     task_id = Column(String, primary_key=True)
#     question = Column("Question", String)
#     level = Column("Level", Integer)
#     final_answer = Column("Final answer", String)
#     file_name = Column("file_name", String)
#     file_path = Column("file_path", String)
#     annotator_metadata = Column("Annotator Metadata", String)
#     split_type = Column("split_type", String)
#     s3_url = Column("s3_url", String)
#     file_extension = Column("file_extension", String)
#     s3_url_extracted_azure = Column("s3_url_extracted_azure", String)
#     s3_url_extracted_pypdf = Column("s3_url_extracted_pypdf", String)