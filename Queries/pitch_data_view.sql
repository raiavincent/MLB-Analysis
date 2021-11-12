SELECT
  pitch_type,
  release_speed,
  release_pos_x,
  release_pos_y,
  release_pos_z,
  pitcher,
  zone,
  p_throws,
  stand,
  type,
  balls,
  strikes,
  outs_when_up,
  inning,
  inning_topbot,
  vx0,
  vy0,
  vz0,
  ax,
  ay,
  az,
  sz_top,
  sz_bot,
  effective_speed,
  release_spin_rate,
  game_pk,
  at_bat_number pitch_number,
  spin_axis,
  CONCAT(game_pk,at_bat_number,pitch_number) AS pitch_id,
  CONCAT(game_pk,at_bat_number) AS at_bat_id,
  CONCAT(game_pk,inning_topbot,inning) AS inning_id,
  MLBNAME AS pitcher_full
FROM
  `valuesheet.MLB.statcast`
LEFT JOIN
  `valuesheet.MLB.player_ids`
ON
  MLBID = pitcher