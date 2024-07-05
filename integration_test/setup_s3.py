import os

# Configure AWS CLI to use LocalStack
os.system("aws configure set aws_access_key_id test")
os.system("aws configure set aws_secret_access_key test")
os.system("aws configure set default.region us-east-1")
os.system("aws configure set default.output json")

# Create an S3 bucket
os.system("aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration")

# Verify the bucket creation
os.system("aws --endpoint-url=http://localhost:4566 s3 ls")
