from sportsipy.mlb.teams import Team
from sportsipy.mlb.teams import Teams
import pandas as pd
import mlbvars
import datevars
import gspread
from datetime import datetime
import mlbSecrets

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

print('Uploading resulting dataframe to google sheets.')
gc = gspread.oauth()

# create the workbook where the day's data will go
# add in folder_id to place it in the folder we want
sh = gc.create(f'MLB Team Data as of {dateString}',folder_id=mlbSecrets.mlbTeamFolderId)

# access the first sheet of that newly created workbook
worksheet = sh.get_worksheet(0)

# edit the worksheet with the created dataframe for the day's data
worksheet.update([league_df.columns.values.tolist()] + league_df.values.tolist())

# open the main workbook with that workbook's url
db = gc.open_by_url(mlbSecrets.teamDashboardURL)

# changed this over to the second sheet so the dashboard can be the first sheet
# dbws is the database worksheet, as in the main workbook that is updated and
# used to analyze and pick from
dbws = db.get_worksheet(1)

# below clears the stock sheet so it can be overwritten with updates
# z1000 is probably overkill but would rather overkill than underkill
range_of_cells = dbws.range('A1:Z1000')
for cell in range_of_cells:
    cell.value = ''
dbws.update_cells(range_of_cells)

# update the spreadsheet in the database workbook with the df
dbws.update([league_df.columns.values.tolist()] + league_df.values.tolist())

print('Script complete.')
