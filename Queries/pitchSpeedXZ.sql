SELECT
  pr.pitch_name,
  ROUND(AVG(pv.plate_x), 4) AS avg_X,
  ROUND(AVG(pv.plate_z), 4) AS avg_Z,
  ROUND(AVG(pv.release_speed), 4) AS avg_speed
FROM
  `valuesheet.MLB.pitching_view` AS pv
LEFT JOIN
  `valuesheet.MLB.hitting_data` AS hd
ON
  pv.pitch_id = hd.pitch_id
LEFT JOIN
  `valuesheet.MLB.pitch_ref` AS pr
ON
  pr.pitch_type = pv.pitch_type
WHERE
  hd.events = 'strikeout'
  AND pv.type IN('S')
  AND pv.pitch_type IS NOT NULL
GROUP BY
  pr.pitch_name
ORDER BY
  avg_speed DESC