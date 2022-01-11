-- Temp function to get year

CREATE TEMP FUNCTION getYear(x DATE)
    RETURNS INT64
    AS (EXTRACT(year FROM x));

SELECT
    getYear(gd.game_date) AS year,
    pv.pitcher_full,
    pr.pitch_name,
    pv.release_speed,
    pv.release_spin_rate,
    pv.plate_x,
    pv.plate_z
FROM 
    `valuesheet.MLB.pitching_view` AS pv
INNER JOIN 
    `valuesheet.MLB.pitch_ref` AS pr ON pv.pitch_type = pr.pitch_type
INNER JOIN 
    `valuesheet.MLB.game_data` AS gd ON pv.game_pk = gd.game_pk
ORDER BY
    release_speed DESC
LIMIT 15 