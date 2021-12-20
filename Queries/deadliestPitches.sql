SELECT
  pv.pitch_type,
  pr.pitch_name,
  ROUND(AVG(pv.release_speed),2) AS avg_speed,
  FORMAT("%'d",COUNT(*)) AS outs
FROM
  `valuesheet.MLB.hitting_data` AS hd
LEFT JOIN
  `valuesheet.MLB.pitching_view` AS pv
ON
  pv.pitch_id = hd.pitch_id
LEFT JOIN
  `valuesheet.MLB.pitch_ref` AS pr
ON
  pv.pitch_type = pr.pitch_type
WHERE
  hd.events = 'strikeout'
  AND pv.type IN('S')
  AND pv.pitch_type IS NOT NULL
GROUP BY
  pv.pitch_type,
  pr.pitch_name
ORDER BY
  COUNT(*) DESC,
  avg_speed DESC