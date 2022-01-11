SELECT
    batter,
    events,
    description,
    stand,
    hit_location,
    bb_type,
    pfx_x,
    pfx_z,
    inning,
    inning_topbot,
    hc_x,
    hc_y,
    hit_distance_sc,
    launch_angle,
    launch_speed,
    launch_speed_angle,
    game_pk,
    at_bat_number,
    pitch_number,
    CONCAT(game_pk,at_bat_number,pitch_number) AS pitch_id,
    CONCAT(game_pk,at_bat_number) AS at_bat_id,
    CONCAT(game_pk,inning_topbot,inning) AS inning_id,
    MLBNAME AS batter_full
FROM 
    `valuesheet.MLB.statcast`
LEFT JOIN `valuesheet.MLB.player_ids`ON MLBID = batter