import os
from dotenv import load_dotenv
load_dotenv()

aws_rds_host = os.getenv('AWS_RDS_HOST')
aws_rds_port = os.getenv('AWS_RDS_DB_PORT')
aws_rds_user = os.getenv('AWS_RDS_USERNAME')
aws_rds_password = os.getenv('AWS_RDS_PASSWORD')
aws_rds_db = os.getenv('AWS_RDS_DATABASE')
aws_profile = os.getenv('AWS_PROFILE')
hf_token = os.getenv('HF_TOKEN')


DATABSE_CONFIG = {
    'host': aws_rds_host,
    'port': aws_rds_port,
    'user': aws_rds_user,
    'password': aws_rds_password,
    'database': aws_rds_db,
}

HF_CONFIG = {
    'token': hf_token
}