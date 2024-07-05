import pandas as pd
from datetime import datetime
import boto3
import os

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

# Define test data (similar to Q3)
data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]
columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df_input = pd.DataFrame(data, columns=columns)

# Save DataFrame to Parquet file
input_file = 'january_2023_data.parquet'
S3_ENDPOINT_URL= 'http://localhost:4566'
options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
}

df_input.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

print(f"Saved DataFrame to {input_file}")

# Verify file existence in S3 using AWS CLI (command-line)
os.system(f"aws --endpoint-url=http://localhost:4566 s3 ls s3://nyc-duration/{input_file}")

# Print the size of the file
file_size = os.path.getsize(input_file)
print(f"Size of {input_file}: {file_size} bytes")
