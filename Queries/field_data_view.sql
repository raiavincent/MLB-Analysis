WITH player_names AS(
  SELECT MLBNAME,MLBID FROM `valuesheet.MLB.player_ids`
)

SELECT
  s.fielder_2 AS catcher,
  s.fielder_3 AS first_baseman,
  s.fielder_4 AS second_baseman,
  s.fielder_5 AS third_baseman,
  s.fielder_6 AS shortstop,
  s.fielder_7 AS left_fielder,
  s.fielder_8 AS center_fielder,
  s.fielder_9 AS right_fielder,
  s.game_pk,
  CONCAT(s.game_pk,s.at_bat_number,s.pitch_number) AS pitch_id,
  CONCAT(s.game_pk,s.at_bat_number) AS at_bat_id,
  CONCAT(s.game_pk,s.inning_topbot,s.inning) AS inning_id,
  catcher_name.MLBNAME AS catcher_full,
  FB_name.MLBNAME AS first_baseman_full,
  SB_name.MLBNAME AS second_baseman_full,
  TB_name.MLBNAME AS third_baseman_full,
  SS_name.MLBNAME AS shortstop_full,
  LF_name.MLBNAME AS left_fielder_full,
  CF_name.MLBNAME AS center_fielder_full,
  RF_name.MLBNAME AS right_fielder_full
FROM
  `valuesheet.MLB.statcast` AS s
LEFT JOIN
  player_names AS catcher_name
ON
  s.fielder_2 = MLBID
LEFT JOIN
  player_names AS FB_name
ON
 s.fielder_3 = FB_name.MLBID
LEFT JOIN
  player_names AS SB_name
ON
  s.fielder_4 = SB_name.MLBID
LEFT JOIN
  player_names AS TB_name
ON
  s.fielder_5 = TB_name.MLBID
LEFT JOIN
  player_names AS SS_name
ON
  s.fielder_6 = SS_name.MLBID
LEFT JOIN
  player_names AS LF_name
ON
  s.fielder_7 = LF_name.MLBID
LEFT JOIN
  player_names AS CF_name
ON
  s.fielder_8 = CF_name.MLBID
LEFT JOIN
  player_names AS RF_name
ON
  s.fielder_9 = RF_name.MLBID