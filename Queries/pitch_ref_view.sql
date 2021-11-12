SELECT
  DISTINCT(pitch_type),
  pitch_name
FROM
  `valuesheet.MLB.statcast`
WHERE
  pitch_type IS NOT NULL