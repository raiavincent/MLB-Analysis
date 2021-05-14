from sportsipy.mlb.teams import Teams
from sportsipy.mlb.roster import Player
from sportsipy.mlb.roster import Roster
import pandas as pd
from datetime import datetime
import gspread
from mlbSecrets import mlbSeasonFolderId, seasonDashboardURL
from mlbSecrets import mlbCareerFolderId, careerDashboardURL
import datevars
import schedule
import time
import numpy as np

def getstats():
    today = datetime.now()
    
    if datevars.start <= today <= datevars.end:
        startTime = datetime.now()
        
        # Function to get player info from Player class object.
        def get_player_df(player):
            # helper function to get year for each row and denote
            # rows that contain career totals.
            def get_year(ix):
                if ix[0] == "Career":
                    return "Career"
                elif ix[0] == "1999-00":
                    return "2000"
                else:
                    return ix[0][0:2] + ix[0][-2:]
            
            # get player df and add some extra info
            player_df = player.dataframe # establish dataframe
            # player_id field is populated with player_id
            player_df['player_id'] = player.player_id 
            player_df['name'] = player.name # name field gets player name
            # year field gets the year of each season pulled
            player_df['year'] = [get_year(ix) for ix in player_df.index] 
            player_df['id'] = [player_id + ' ' + year for player_id,
                           year in zip(player_df['player_id'],
                           player_df['year'])]
            player_df.set_index('player_id', drop = True, inplace = True)
            
            
            return player_df
        
        # initialize a list of players that we have pulled data for
        players_collected = []
        season_df_init = 0
        career_df_init = 0
        season_df = 0
        career_df = 0
        years = [datevars.season]
        # iterate through years.
        for year in years:
            print('\n' + str(year))
                
            # iterate through all teams in that year.
            for team in Teams(year = str(year)).dataframes.index:
                print('\n' + team + '\n')
                
                # iterate through every player on a team roster.
                for player_id in Roster(team, year = year,
                                 slim = True).players.keys():
                    
                    # only pull player info if that player hasn't
                    # been pulled already.
                    if player_id not in players_collected:
                        try:
                            player = Player(player_id)
                            player_info = get_player_df(player)
                            player_seasons = player_info[
                                             player_info['year'] != "Career"]
                            player_career = player_info[
                                            player_info['year'] == "Career"]
                        except Exception:
                            pass
                        # create season_df if not initialized
                        if not season_df_init:
                            try:
                                season_df = player_seasons
                                season_df_init = 1
                            except Exception:
                                pass
                        # else concatenate to season_df
                        else:
                            try:
                                season_df = pd.concat([season_df,
                                               player_seasons], axis = 0)
                            except Exception:
                                pass
                        if not career_df_init:
                            try:
                                career_df = player_career
                                career_df_init = 1
                            except Exception:
                                pass
                        # else concatenate to career_df
                        else:
                            try:
                                career_df = pd.concat([career_df,
                                               player_career], axis = 0)
                            except Exception:
                                pass
        
                        # add player to players_collected
                        players_collected.append(player_id)
                        print(player.name)
        
        currentSeason = season_df[season_df['year'] == datevars.season]
        currentSeason = currentSeason.sort_values(by='name',ascending=True)
        
        season_df = season_df.loc[:,~season_df.columns.duplicated()]
        currentSeason = currentSeason.loc[:,~currentSeason.columns.duplicated()]
        currentSeason = currentSeason.loc[:, (currentSeason != 0).any(axis=0)]
        # need to fill NA values as it was causing errors for gspread
        currentSeason.fillna('', inplace=True)
        career_df.fillna('',inplace=True)
        currentSeason = currentSeason.replace('\n',' ', regex=True)
        career_df = career_df.replace('\n',' ', regex=True)
        
        # df1 = df.where((pd.notnull(df)), None)
        currentSeason.where((pd.notnull(currentSeason)), None)
        career_df.where((pd.notnull(career_df)), None)
        
        currentSeason.replace(np.NaN, '', inplace=True)
        career_df.replace(np.NaN, '', inplace=True)
        
        currentSeason = currentSeason.astype(str)
        career_df = career_df.astype(str)
        
        dateString = datetime.strftime(datetime.now(), '%Y_%m_%d')
        
        # gc authorizes and lets us access the spreadsheets
        gc = gspread.oauth()
        
        # create the workbook where the day's data will go
        # add in folder_id to place it in the folder we want
        shP = gc.create(f'{datevars.season} Player Data as of {dateString}',folder_id=mlbSeasonFolderId)
        shC = gc.create(f'Active Player Career Data as of {dateString}',folder_id=mlbCareerFolderId)
        
        # access the first sheet of that newly created workbook
        worksheetP = shP.get_worksheet(0)
        worksheetC = shC.get_worksheet(0)
        
        # edit the worksheet with the created dataframe for the day's data
        # worksheetP.update([currentSeason.columns.values.tolist()] + currentSeason.values.tolist())
        # worksheetC.update([career_df.columns.values.tolist()] + career_df.values.tolist())
        
        worksheetP.update(
        [currentSeason.columns.values.tolist()] + [[vv if pd.notnull(vv) else '' for vv in ll] for ll in currentSeason.values.tolist()]
        )

        worksheetC.update(
        [career_df.columns.values.tolist()] + [[vv if pd.notnull(vv) else '' for vv in ll] for ll in career_df.values.tolist()]
        )
        
        # open the main workbook with that workbook's url
        dbP = gc.open_by_url(seasonDashboardURL)
        dbC = gc.open_by_url(careerDashboardURL)
        
        # changed this over to the second sheet so the dashboard can be the first sheet
        # dbws is the database worksheet, as in the main workbook that is updated and
        # used to analyze and pick from
        dbwsP = dbP.get_worksheet(1)
        dbwsC = dbC.get_worksheet(1)
        
        # below clears the sheet so it can be overwritten with updates
        # z1000 is probably overkill but would rather overkill than underkill
        range_of_cells = dbwsP.range('A1:Z10000')
        for cell in range_of_cells:
            cell.value = ''
        dbwsP.update_cells(range_of_cells)
        
        range_of_cells = dbwsC.range('A1:Z10000')
        for cell in range_of_cells:
            cell.value = ''
        dbwsC.update_cells(range_of_cells)
        
        # update the sheet in the database workbook with the df
        dbwsP.update([currentSeason.columns.values.tolist()] + currentSeason.values.tolist())
        dbwsC.update([career_df.columns.values.tolist()] + career_df.values.tolist())
        
        # unstringify the strung data for SQL purposes
        spreadsheetIdS = seasonDashboardURL  # Please set the Spreadsheet ID.
        sheetName = "Data"  # Please set the sheet name.
        
        spreadsheetS = gc.open_by_url(spreadsheetIdS)
        sheetIdS = spreadsheetS.worksheet(sheetName)._properties['sheetId']
        
        requestsS = {
            "requests": [
                {
                    "findReplace": {
                        "sheetId": sheetIdS,
                        "find": "^'",
                        "searchByRegex": True,
                        "includeFormulas": True,
                        "replacement": ""
                    }
                }
            ]
        }
        
        spreadsheetS.batch_update(requestsS)
        
        spreadsheetIdC = careerDashboardURL  # Please set the Spreadsheet ID.
        sheetName = "Data"  # Please set the sheet name.
        
        spreadsheetC = gc.open_by_url(spreadsheetIdC)
        sheetIdC = spreadsheetC.worksheet(sheetName)._properties['sheetId']
        
        requestsC = {
            "requests": [
                {
                    "findReplace": {
                        "sheetId": sheetIdC,
                        "find": "^'",
                        "searchByRegex": True,
                        "includeFormulas": True,
                        "replacement": ""
                    }
                }
            ]
        }
        
        spreadsheetC.batch_update(requestsC)
        
        print(datetime.now()-startTime)
    else:
        print('We are not within the date range to run getpPlayerStatsMLB.py. Please check datevars.py for MLB-Analysis is updated for the next season.')

schedule.every().day.at("05:00").do(getstats)

while True:
    schedule.run_pending()
    time.sleep(1)           