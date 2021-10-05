from sportsipy.mlb.teams import Team
from sportsipy.mlb.teams import Teams
import pandas as pd
import mlbvars
import datevars
import gspread
from datetime import datetime
import mlbSecrets

today = datetime.now()

if datevars.start <= today <= datevars.end:
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
        
    # calculate ewp
    print('Running EWP calculations.')
    
    league_df['ewp'] = round(((league_df['runs']**mlbvars.exponent)/
    ((league_df['runs']**mlbvars.exponent)+(league_df['runs_against']**mlbvars.exponent))),2)
    league_df['pw'] = league_df['games'] * league_df['ewp']
    league_df['pw'] = league_df['pw'].apply(lambda x: round(x, mlbvars.decimals))
    league_df['pl'] = league_df['games'] * (1-league_df['ewp'])
    league_df['pl'] = league_df['pl'].apply(lambda x: round(x, mlbvars.decimals))
    league_df['pw_season'] = mlbvars.gamesInSeason * league_df['ewp']
    league_df['pw_season'] = league_df['pw_season'].apply(lambda x: round(x,mlbvars.decimals))
    league_df['pl_season'] = mlbvars.gamesInSeason * (1-league_df['ewp'])
    league_df['pl_season'] = league_df['pl_season'].apply(lambda x: round(x,mlbvars.decimals))
    league_df['ahead/behind'] = league_df['wins'] - league_df['pw']
    
    # calculate differentials
    print('Calculating differentials.')
    
    league_df['runs/g'] = league_df['runs']/league_df['games']
    league_df['runs_against/g'] = league_df['runs_against']/league_df['games']
    league_df['runs/g'] = league_df['runs/g'].apply(lambda x: round(x,2))
    league_df['runs_against/g'] = league_df['runs_against/g'].apply(lambda x: round(x,2))
    league_df['runs/g_diff'] = league_df['runs/g']-league_df['runs_against/g']
    league_df['runs_diff'] = league_df['runs']-league_df['runs_against']
    
    league_df = league_df.reindex(sorted(league_df.columns), axis=1)
    
    dateString = datetime.strftime(datetime.now(), '%Y_%m_%d')
    
    print('Script complete.')

else:
    print('We are not within the date range to run createDfMLB.py. Please check datevars.py for MLB-Analysis is updated for the next season.')
        