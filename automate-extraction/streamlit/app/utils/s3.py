# import boto3
from urllib.parse import urlparse

def parse_s3_url(s3_url):
    parsed_url = urlparse(s3_url)
    if parsed_url.netloc.endswith('.s3.amazonaws.com'):
        bucket_name = parsed_url.netloc.split('.')[0]
        object_key = parsed_url.path.lstrip('/')
        return bucket_name, object_key
    else:
        raise ValueError("Invalid S3 URL format.")
    
# def generate_presigned_url(bucket_name, object_key, expiration=3600):
#     s3 = boto3.client('s3', aws_profile='dev')
#     try:
#         response = s3.generate_presigned_url(
#             'get_object',
#             Params={'Bucket': bucket_name, 'Key': object_key},
#             ExpiresIn=expiration
#         )
#         return response
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None