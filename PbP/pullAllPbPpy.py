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
    
    dataPbP = pd.to_datetime(dataPbP['game_date'])
    
    dataPbP = dataPbP.astype({'id':int,
                  'pitch_type':str,
                  'release_speed':float,
                  'release_pos_x':float,
                  'release_pos_z':float,
                  'player_name':str,
                  'batter':int,
                  'pitcher':int,
                  'events':str,
                  'description':str,
                  'spin_dir':str,
                  'spin_rate_deprecated':str,
                  'break_angle_deprecated':str,
                  'break_length_deprecated':str,
                  'zone':int,
                  'des':str,
                  'game_type':str,
                  'stand':str,
                  'p_throws':str,
                  'type':str,
                  'home_team':str,
                  'away_team':str,
                  'hit_location':int,
                  'bb_type':str,
                  'balls':int,
                  'strikes':int,
                  'game_year':int,
                  'pfx_x':float,
                  'pfx_z':float,
                  'plate_x':float,
                  'plate_z':float,
                  'on_3b':int,
                  'on_2b':int,
                  'on_1b':int,
                  'outs_when_up':int,
                  'inning':int,
                  'inning_topbot':str,
                  'hc_x':float,
                  'hc_y':float,
                  'tfs_deprecated':str,
                  'tfs_zulu_deprecated':str,
                  'fielder_2':int,
                  'umpire':str,
                  'sv_id':str,
                  'vx0':float,
                  'vy0':float,
                  'vz0':float,
                  'ax':float,
                  'ay':float,
                  'az':float,
                  'sz_top':float,
                  'sz_bot':float,
                  'hit_distance_sc':int,
                  'launch_speed':float,
                  'launch_angle':int,
                  'effective_speed':float,
                  'release_spin_rate':int,
                  'release_extension':float,
                  'game_pk':int,
                  'pitcher_1':int,
                  'fielder_2_1':int,
                  'fielder_3':int,
                  'fielder_4':int,
                  'fielder_5':int,
                  'fielder_6':int,
                  'fielder_7':int,
                  'fielder_8':int,
                  'fielder_9':int,
                  'release_pos_y':float,
                  'estimated_ba_using_speedangle':float,
                  'estimated_woba_using_speedangle':float,
                  'woba_value':float,
                  'woba_denom':int,
                  'babip_value':int,
                  'iso_value':int,
                  'launch_speed_angle':int,
                  'at_bat_number':int,
                  'pitch_number':int,
                  'pitch_name':str,
                  'home_score':int,
                  'away_score':int,
                  'bat_score':int,
                  'fld_score':int,
                  'post_away_score':int,
                  'post_home_score':int,
                  'post_bat_score':int,
                  'post_fld_score':int,
                  'if_fielding_alignment':str,
                  'of_fielding_alignment':str,
                  'spin_axis':int,
                  'delta_home_win_exp':float,
                  'delta_run_exp':float
                  })
    
    # list(dataPbP.columns)
    
    # print(dataPbP.head)
    
    # save as csv for upload/distribution
    # dataPbP.to_csv('2015 Start PbP.csv')
    
    print('Uploading.')
    
    pandas_gbq.to_gbq(
    dataPbP, table_id, project_id=project_id, if_exists='append')

if __name__ == '__main__':
    pullData()