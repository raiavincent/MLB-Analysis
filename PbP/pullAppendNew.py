# DONE pull down 'yesterday' data
# DONE setup to_gbq
# DONE to_gbq as append
# DONE get and set project_id from GCP
# DONE get and set table_id to the full destination table ID
# DONE set credentials
# TODO set dtypes of dataPbPYest to table schema

import pybaseball
from pybaseball import statcast
import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
# from statcast_table_schema import statcast_schema

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
    
    # dataPbPYest.index.name = 'id'
    
    dataPbPYest = dataPbPYest.rename(columns={'pitcher.1':'pitcher_1',
                                'fielder_2.1':'fielder_2_1'})
    
    # dataPbPYest = pd.to_datetime(dataPbPYest['game_date'])
    
    # dataPbPYest = dataPbPYest.astype({'id':int,
    #               'pitch_type':str,
    #               'release_speed':float,
    #               'release_pos_x':float,
    #               'release_pos_z':float,
    #               'player_name':str,
    #               'batter':int,
    #               'pitcher':int,
    #               'events':str,
    #               'description':str,
    #               'spin_dir':str,
    #               'spin_rate_deprecated':str,
    #               'break_angle_deprecated':str,
    #               'break_length_deprecated':str,
    #               'zone':int,
    #               'des':str,
    #               'game_type':str,
    #               'stand':str,
    #               'p_throws':str,
    #               'type':str,
    #               'home_team':str,
    #               'away_team':str,
    #               'hit_location':int,
    #               'bb_type':str,
    #               'balls':int,
    #               'strikes':int,
    #               'game_year':int,
    #               'pfx_x':float,
    #               'pfx_z':float,
    #               'plate_x':float,
    #               'plate_z':float,
    #               'on_3b':int,
    #               'on_2b':int,
    #               'on_1b':int,
    #               'outs_when_up':int,
    #               'inning':int,
    #               'inning_topbot':str,
    #               'hc_x':float,
    #               'hc_y':float,
    #               'tfs_deprecated':str,
    #               'tfs_zulu_deprecated':str,
    #               'fielder_2':int,
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
    #               'hit_distance_sc':int,
    #               'launch_speed':float,
    #               'launch_angle':int,
    #               'effective_speed':float,
    #               'release_spin_rate':int,
    #               'release_extension':float,
    #               'game_pk':int,
    #               'pitcher_1':int,
    #               'fielder_2_1':int,
    #               'fielder_3':int,
    #               'fielder_4':int,
    #               'fielder_5':int,
    #               'fielder_6':int,
    #               'fielder_7':int,
    #               'fielder_8':int,
    #               'fielder_9':int,
    #               'release_pos_y':float,
    #               'estimated_ba_using_speedangle':float,
    #               'estimated_woba_using_speedangle':float,
    #               'woba_value':float,
    #               'woba_denom':int,
    #               'babip_value':int,
    #               'iso_value':int,
    #               'launch_speed_angle':int,
    #               'at_bat_number':int,
    #               'pitch_number':int,
    #               'pitch_name':str,
    #               'home_score':int,
    #               'away_score':int,
    #               'bat_score':int,
    #               'fld_score':int,
    #               'post_away_score':int,
    #               'post_home_score':int,
    #               'post_bat_score':int,
    #               'post_fld_score':int,
    #               'if_fielding_alignment':str,
    #               'of_fielding_alignment':str,
    #               'spin_axis':int,
    #               'delta_home_win_exp':float,
    #               'delta_run_exp':float
    #               })
    
    # print(dataPbPYest.head())
    
    # print(dataPbPYest.dtypes)
    
    # print(list(dataPbPYest.columns))
    
    # print(dataPbPYest.head)
    
    pandas_gbq.to_gbq(
        dataPbPYest, table_id, project_id=project_id, if_exists='append')
    
if __name__ == '__main__':
    pullNewData()