CREATE TEMP FUNCTION decround (x FLOAT64) AS (
  ROUND(x,2)
);

WITH totalRuns AS (SELECT
    SUM((post_bat_score - bat_score)) AS runsScored
FROM 
    `valuesheet.MLB.hitting_data`
)

SELECT
    inning,
    CONCAT(inning_topbot,inning) AS inningHalf,
    events,
    SUM(post_bat_score - bat_score) AS runsScored,
    decround(((SUM(post_bat_score - bat_score)/
    (SELECT runsScored FROM totalRuns))*100)) AS pctruns
FROM 
    `valuesheet.MLB.hitting_data` AS hd
WHERE
    events IN ('single','double','triple','home_run') -- only bring in RBIs
    AND (post_bat_score - bat_score) > 0 -- make sure we only have events where there is a run scored
    AND inning <= 9 -- do not care too much about extra innings
GROUP BY
    inning,
    inningHalf,
    events
ORDER BY 
    inning,
    inningHalf DESC