# TODO find earliest date of data
# DONE fix spawn main
# TODO create table directly from here
# TODO check and rename column names

import pybaseball
from pybaseball import statcast
from datetime import datetime
from google.oauth2 import service_account
import pandas_gbq
import pandas as pd
from pandas_gbq import schema
from statcast_table_schema import statcast_schema

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
    
    dataPbP = dataPbP.astype({'game_date':str})
    
    # dataPbP = dataPbP.drop(columns=['id'])
    
    # dataPbP = pd.to_datetime(dataPbP['game_date'])
    
    # dataPbP = dataPbP.astype({
    #               'pitch_type':str,
    #               'release_speed':float,
    #               'release_pos_x':float,
    #               'release_pos_z':float,
    #               'player_name':str,
    #               'batter':"Int64",
    #               'pitcher':"Int64",
    #               'events':str,
    #               'description':str,
    #               'spin_dir':str,
    #               'spin_rate_deprecated':str,
    #               'break_angle_deprecated':str,
    #               'break_length_deprecated':str,
    #               'zone':"Int64",
    #               'des':str,
    #               'game_type':str,
    #               'stand':str,
    #               'p_throws':str,
    #               'home_team':str,
    #               'away_team':str,
    #               'hit_location':"Int64",
    #               'bb_type':str,
    #               'balls':"Int64",
    #               'strikes':"Int64",
    #               'game_year':"Int64",
    #               'pfx_x':float,
    #               'pfx_z':float,
    #               'plate_x':float,
    #               'plate_z':float,
    #               'on_3b':"Int64",
    #               'on_2b':"Int64",
    #               'on_1b':"Int64",
    #               'outs_when_up':"Int64",
    #               'inning':"Int64",
    #               'inning_topbot':str,
    #               'hc_x':float,
    #               'hc_y':float,
    #               'tfs_deprecated':str,
    #               'tfs_zulu_deprecated':str,
    #               'fielder_2':"Int64",
    #               'umpire':str,
    #               'sv_id':str,
    #               'vx0':float,
    #               'vy0':float,
    #               'vz0':float,
    #               'ax':float,
    #               'ay':float,
    #               'az':float,
    #               'sz_top':float,
    #               'sz_bot':float,
    #               'hit_distance_sc':"Int64",
    #               'launch_speed':float,
    #               'launch_angle':"Int64",
    #               'effective_speed':float,
    #               'release_spin_rate':"Int64",
    #               'release_extension':float,
    #               'game_pk':"Int64",
    #               'pitcher_1':"Int64",
    #               'fielder_2_1':"Int64",
    #               'fielder_3':"Int64",
    #               'fielder_4':"Int64",
    #               'fielder_5':"Int64",
    #               'fielder_6':"Int64",
    #               'fielder_7':"Int64",
    #               'fielder_8':"Int64",
    #               'fielder_9':"Int64",
    #               'release_pos_y':float,
    #               'estimated_ba_using_speedangle':float,
    #               'estimated_woba_using_speedangle':float,
    #               'woba_value':float,
    #               'woba_denom':"Int64",
    #               'babip_value':"Int64",
    #               'iso_value':"Int64",
    #               'launch_speed_angle':"Int64",
    #               'at_bat_number':"Int64",
    #               'pitch_number':"Int64",
    #               'pitch_name':str,
    #               'home_score':"Int64",
    #               'away_score':"Int64",
    #               'bat_score':"Int64",
    #               'fld_score':"Int64",
    #               'post_away_score':"Int64",
    #               'post_home_score':"Int64",
    #               'post_bat_score':"Int64",
    #               'post_fld_score':"Int64",
    #               'if_fielding_alignment':str,
    #               'of_fielding_alignment':str,
    #               'spin_axis':"Int64",
    #               'delta_home_win_exp':float,
    #               'delta_run_exp':float,
    #               'game_date':str
    #               })
    
    # schema.generate_bq_schema(dataPbP)
    
    print(dataPbP.info(verbose=True))
    
    # list(dataPbP.columns)
    
    # pr"Int64"(dataPbP.head)
    
    # save as csv for upload/distribution
    # dataPbP.to_csv('2015 Start PbP.csv')
    
    print('Uploading.')
    
    pandas_gbq.to_gbq(
    dataPbP, table_id, project_id=project_id, if_exists='append',table_schema=statcast_schema)

if __name__ == '__main__':
    pullData()