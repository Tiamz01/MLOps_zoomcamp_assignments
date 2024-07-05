import pytest
import pandas as pd
from datetime import datetime
import sys
import os

# Add the directory where 'batch.py' is located to the system path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import batch


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():
    # Define test data directly in the test function
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    
    categorical_columns = ['PULocationID', 'DOLocationID']

    # Call the function under test
    actual_df = batch.read_data(df, categorical_columns)

    expected_data = [
        ('3', '-1', dt(1, 1), dt(1, 10), 9.0),
        ('5', '1', dt(1, 2), dt(1, 10), 6.0),
    ]
    expected_columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'duration']
    expected_df = pd.DataFrame(expected_data, columns=expected_columns)

    assert actual_df.shape == expected_df.shape
    print(f"actual_df shape is:{actual_df.shape}")
    print(f"expected_df shape is:{expected_df.shape} ")


if __name__ == "__main__":
    test_prepare_data()
