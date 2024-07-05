import pandas as pd
from datetime import datetime 


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def read_data(df, categorical):
    df['duration'] = df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def prepare_data():
    
    data = [
                (None, None, dt(1, 1), dt(1, 10)),
                (1, 1, dt(1, 2), dt(1, 10)),
                (1, None, dt(1, 2, 0), dt(1, 2, 59)),
                (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
            ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    
    categorical = ['PULocationID', 'DOLocationID']
    actual_df = read_data(df, categorical)


    expected_data = [
            ('-1', '-1', dt(1, 1), dt(1, 10), 9.0),
            ('1', '1', dt(1, 2), dt(1, 10), 8.0),
        ]

    expected_columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'duration']
    expected_df = pd.DataFrame(expected_data, columns=expected_columns)
    
    
    assert actual_df.shape == expected_df.shape
    print(f'actual_df.shape:{actual_df.shape}')
    print(f'expected_df.shape:{expected_df.shape}')

if __name__ == "__main__":
    prepare_data()
    



