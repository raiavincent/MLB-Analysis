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
from creds import credentialsPath
from creds import projectid
from creds import tableid
from datetime import date
import schedule
import time
import importlib

project_id = projectid
table_id = tableid
credentials = (
    service_account.Credentials.from_service_account_file(credentialsPath))

def pullData():
    
    importlib.reload(statcast_schema)
    
    today = date.today()
    print("Today's date:", today)

    # enable cache, helps in case of crashing when pulling large amounts 
    # of data
    pybaseball.cache.enable()
    
    # not including any dates, automatically uses yesterday as start and today
    # as the end
    dataPbP = statcast()
    
    dataPbP.index.name = 'id'
    dataPbP['id'] = dataPbP.index
    dataPbP = dataPbP.rename(columns={'pitcher.1':'pitcher_1',
                                'fielder_2.1':'fielder_2_1'})
    
    # recast date as string to allow for upload to BQ
    dataPbP = dataPbP.astype({'game_date':str})
    
    print('Uploading.')
    
    pandas_gbq.to_gbq(
    dataPbP, table_id, project_id=project_id, if_exists='append',
    table_schema=statcast_schema)


schedule.every().day.at(("06:00")).do(pullData)

while True:
    schedule.run_pending()
    time.sleep(1)
