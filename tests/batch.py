#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd




def read_data(file, categorical):
    options = {
        'client_kwargs': {
            'endpoint_url': 'http://localhost:4566'  # Adjust based on your S3 endpoint
        }
    }
    
    if isinstance(file, pd.DataFrame):
        df = file.copy()  # Use a copy to avoid modifying the original DataFrame
    elif isinstance(file, str) and file.endswith(".parquet"):
        try:
            # Read Parquet file from S3
            df = pd.read_parquet(f's3://bucket/{file}', storage_options=options)
        except Exception as e:
            print(f"Error reading Parquet file {file} from S3: {e}")
            df = pd.DataFrame()  # Return an empty DataFrame on error
    else:
        try:
            # Attempt to create a DataFrame from other types of input
            df = pd.DataFrame(file)
        except Exception as e:
            print(f"Error creating DataFrame from {file}: {e}")
            df = pd.DataFrame()  # Return an empty DataFrame on error
    
    df['duration'] = df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration-prediction-alexey/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def main(year, month):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)
    categorical = ['PULocationID', 'DOLocationID']

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)


    df = read_data(input_file, categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)


    print('predicted mean duration:', y_pred.mean())


    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred


    df_result.to_parquet(output_file, engine='pyarrow', index=False)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        main(year, month)
