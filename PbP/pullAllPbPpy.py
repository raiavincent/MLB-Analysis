# DONE find earliest date of data
# DONE fix spawn main
# DONE create table directly from here
# DONE check and rename column names

import pybaseball
from pybaseball import statcast
from google.oauth2 import service_account
import pandas_gbq
import pandas as pd
from statcast_table_schema import statcast_schema

project_id = 'valuesheet'
table_id = 'MLB.statcast'
credentials = service_account.Credentials.from_service_account_file(
    r'C:\Users\Vincent\Documents\GitHub\MLB-Analysis\PbP\valuesheet-64e2835ccf11.json')

def pullData():
    
    # enable cache, helps in case of crashing when pulling large amounts 
    # of data
    pybaseball.cache.enable()
    
    # pulling all data from 2015 seaason through today
    dataPbP = statcast(start_dt='2015-01-01', end_dt='2021-12-17')
    
    dataPbP.index.name = 'id'
    dataPbP['id'] = dataPbP.index
    dataPbP = dataPbP.rename(columns={'pitcher.1':'pitcher_1',
                                'fielder_2.1':'fielder_2_1'})
    
    # recast date as string to allow for upload to BQ
    dataPbP = dataPbP.astype({'game_date':str})
    
    dataPbP = dataPbP.drop_duplicates() # drop any duplicates to prevent any extra work on sql and pbi end
    
    print('Uploading.')
    
    # print(dataPbP)
    
    pandas_gbq.to_gbq(
    dataPbP, table_id, project_id=project_id, if_exists='append',table_schema=statcast_schema)

if __name__ == '__main__':
    pullData()
