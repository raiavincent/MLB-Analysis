# TODO find earliest date of data
# DONE fix spawn main
# TODO create table directly from here
# TODO check and rename column names

import pybaseball
from pybaseball import statcast
from datetime import datetime
from google.oauth2 import service_account
import pandas_gbq

project_id = 'valuesheet'
table_id = 'MLB.statcast'
credentials = service_account.Credentials.from_service_account_file(
    r'C:\Users\Vincent\Documents\GitHub\MLB-Analysis\PbP\valuesheet-64e2835ccf11.json')

def pullData():
    # get dates necessary for data pulling
    today = datetime.today()
    todaystr = today.strftime('%Y-%m-%d')
    start_date = '2021-10-08'
    
    # enable cache, helps in case of crashing when pulling large amounts 
    # of data
    pybaseball.cache.enable()
    
    # pulling all data from 2015 seaason through today
    dataPbP = statcast(start_dt=start_date, end_dt=todaystr)
    
    dataPbP.index.name = 'id'
    dataPbP['id'] = dataPbP.index
    dataPbP = dataPbP.rename(columns={'pitcher.1':'pitcher_1',
                                'fielder_2.1':'fielder_2_1'})
    
    # list(dataPbP.columns)
    
    # print(dataPbP.head)
    
    # save as csv for upload/distribution
    # dataPbP.to_csv('2015 Start PbP.csv')
    
    print('Uploading.')
    
    pandas_gbq.to_gbq(
    dataPbP, table_id, project_id=project_id, if_exists='append')

if __name__ == '__main__':
    pullData()