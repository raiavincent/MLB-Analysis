# DONE pull down 'yesterday' data
# TODO setup to_gbq
# FONE to_gbq as append
# TODO get and set project_id from GCP
# TODO get and set table_id to the full destination table ID
# TODO set credentials

import pybaseball
from pybaseball import statcast
import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
from statcast_table_schema import statcast_schema

project_id = 'valuesheet'
table_id = 'MLB.statcast'
credentials = service_account.Credentials.from_service_account_file(
    r'C:\Users\Vincent\Documents\GitHub\MLB-Analysis\PbP\valuesheet-64e2835ccf11.json')

def pullNewData():
    # enable cache, helps in case of crashing when pulling large amounts 
    # of data
    pybaseball.cache.enable()
    
    # pull yesterday data, by not supplying dates, pulls yesterday by  default
    dataPbPYest = statcast()
    
    dataPbPYest.index.name = 'id'
    
    # dataPbPYest.rename(columns={'type':'type1'})
    
    # print(dataPbPYest.head())
    
    # print(dataPbPYest.dtypes)
    
    pandas_gbq.to_gbq(
        dataPbPYest, table_id, project_id=project_id, if_exists='append',
        table_schema=statcast_schema)
    
if __name__ == '__main__':
    pullNewData()