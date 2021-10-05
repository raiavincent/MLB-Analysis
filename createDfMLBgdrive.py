from sportsipy.mlb.teams import Team
from sportsipy.mlb.teams import Teams
import pandas as pd
import mlbvars
import datevars
import gspread
from datetime import datetime
import mlbSecrets
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from gcloud import storage

today = datetime.now()

if datevars.start <= today <= datevars.end:
    client = storage.Client()
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    gauth.LoadCredentialsFile("mycreds.txt")
    print('Running createDfMLB.py')
    # need to get teams
    teams = Teams(year=datevars.season)
    
    # get list of teams to iterate over
    abbr_list = []
    for team in teams:
        abbr_list.append(team.abbreviation)
    
    # establish dataframe for team stats
    league_df = pd.DataFrame()
    
    print('Gathering team statistics.')
    # iterate over the abbrevations to get each teams dataframe
    for abbr in abbr_list:
        nextTeam = Team(abbr)
        team_df = pd.DataFrame(data=nextTeam.dataframe)
        # concatenate onto the established dataframe
        league_df = pd.concat([league_df,team_df])
    
    league_df.to_csv('MLB Team Data.csv',index=False)
    
    bucket = client.get_bucket('raiavincent')
    blob = bucket.blob('MLB Team Data.csv')
    
    # credentials = GoogleCredentials.get_application_default()
    # service = discovery.build('storage', 'v1', credentials=credentials)
    
    # filename = 'MLB Team Data.csv'
    # bucket = 'raiavincent'
    
    # body = {'name': 'MLB Team Data.csv'}
    # req = service.objects().insert(bucket=bucket, body=body, media_body=filename)
    # resp = req.execute()
        
    # file_list = drive.ListFile({'q':"'1-XmAgSJiaVXdjS1db6tPoQC8qipBqye-'  in parents and  trashed=False"}).GetList()
    # file = 'MLB Team Data.csv'
    
    # for file1 in file_list:
    #     if file1['title'] == file:
    #         file1.Delete()   
            
    # f = drive.CreateFile({'parents': [{'id': '1-XmAgSJiaVXdjS1db6tPoQC8qipBqye-'}]})
    # f.SetContentFile(file)
    # f.Upload()
    
    # file2 = drive.CreateFile({'parents': [{'id': '1-XmAgSJiaVXdjS1db6tPoQC8qipBqye-'}]})
    # file2.SetContentFile('MLB Team Data.csv')
    # file2.Patch()
    
    print('Script complete.')

else:
    print('We are not within the date range to run createDfMLB.py. Please check datevars.py for MLB-Analysis is updated for the next season.')
        