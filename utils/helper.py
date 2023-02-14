from typing import List
import pandas as pd
from math import log10, floor
import os

def round_to_sf(x, n):
    return round(x, -int(floor(log10(abs(x))))+n-1)


def read_files_from_s3(s3_paths: List[str]) -> pd.DataFrame:
    df = pd.concat([pd.read_csv(s3_path) for s3_path in s3_paths])
    
    return df


def transform(s3_billing_dataframe: pd.DataFrame):
    storage_services = s3_billing_dataframe.loc[s3_billing_dataframe['Charge description'].str.contains('storage')]
    storage_services = storage_services[['Service','Usage amount']]
    storage_services.loc[(storage_services.Service == 'Amazon Elastic Compute Cloud'), 'Service'] = 'Amazon Elastic Block Store'
    storage_services['Usage amount'] = storage_services['Usage amount'].astype(float)
    storage_services = storage_services.groupby('Service').sum()
    storage_services['Percent'] = storage_services['Usage amount']/storage_services['Usage amount'].sum()*100
    storage_services['Service'] = storage_services.index
    storage_services.Percent = storage_services.Percent.apply(lambda percent: str(round_to_sf(percent, 4)) + '%')
    storage_services['Usage amount'] = storage_services['Usage amount'].apply(lambda usage_amount: str(round_to_sf(usage_amount, 4))+'GB')
    return storage_services.to_dict(orient='records')

def transform_s3_files(s3_paths):
    df = read_files_from_s3(s3_paths)
    return transform(df)