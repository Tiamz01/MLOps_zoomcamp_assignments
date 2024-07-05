#!/bin/bash

# Activate Pipenv environment
pipenv shell

# Install dependencies (if not already installed)
pipenv install

# Start LocalStack with Docker Compose
docker-compose up -d

# Wait for LocalStack to initialize (adjust sleep time based on your system)
sleep 5

# Create S3 bucket in LocalStack
echo "Creating S3 bucket in LocalStack..."
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-local-s3-bucket

# Run integration test script
python integration_test.py

# Verify uploaded file in S3 using AWS CLI
aws --endpoint-url=http://localhost:4566 s3 ls s3://my-local-s3-bucket/

# Stop LocalStack containers after testing
docker-compose down
