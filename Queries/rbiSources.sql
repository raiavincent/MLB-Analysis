SELECT
    inning,
    CONCAT(inning_topbot,inning) AS inningHalf,
    events,
    SUM(post_bat_score - bat_score) AS runsScored 
FROM 
    `valuesheet.MLB.hitting_data` 
WHERE
    events IN('single','double','triple','homerun')
    AND (post_bat_score - bat_score) > 0
    AND inning <= 9
GROUP BY
    inning,
    inningHalf,
    events
ORDER BY 
    inning,
    inningHalf DESC
