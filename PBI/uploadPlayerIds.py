import pandas as pd
import pandas_gbq
from google.oauth2 import service_account

project_id = 'valuesheet'
table_id = 'MLB.player_ids'
credentials = service_account.Credentials.from_service_account_file(
    r'C:\Users\Vincent\Documents\GitHub\MLB-Analysis\PbP\valuesheet-64e2835ccf11.json')

playerIds = pd.read_excel('SFBB-Player-ID-Map.xlsx')

pandas_gbq.to_gbq(playerIds, table_id, project_id=project_id, if_exists='append')