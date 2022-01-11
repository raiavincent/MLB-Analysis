SELECT DISTINCT
    game_date,
    game_pk,
    home_team,
    away_team,
    game_type
FROM `valuesheet.MLB.statcast`
ORDER BY game_date DESC