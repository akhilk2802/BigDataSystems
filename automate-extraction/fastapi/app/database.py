from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
from dotenv import load_dotenv
load_dotenv()

aws_db_user = os.getenv("AWS_RDS_USERNAME")
aws_db_password = os.getenv("AWS_RDS_PASSWORD")
aws_db_host = os.getenv("AWS_RDS_HOST")
aws_db_port = os.getenv("AWS_RDS_DB_PORT")
aws_db_name = os.getenv("AWS_RDS_DATABASE")

# DATABASE_URL = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
DATABASE_URL = f"postgresql://{aws_db_user}:{aws_db_password}@{aws_db_host}:{aws_db_port}/{aws_db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()