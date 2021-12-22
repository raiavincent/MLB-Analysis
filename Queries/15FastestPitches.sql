SELECT
    pv.pitcher_full,
    pr.pitch_name,
    pv.release_speed,
    pv.plate_x,
    pv.plate_z
FROM 
    `valuesheet.MLB.pitching_view` AS pv
INNER JOIN 
    `valuesheet.MLB.pitch_ref` AS pr ON pv.pitch_type = pr.pitch_type
ORDER BY
    release_speed DESC
LIMIT 15 
