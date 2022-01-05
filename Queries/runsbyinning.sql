CREATE TEMP FUNCTION decround (x FLOAT64) AS (
  ROUND(x,2)
);

WITH rawruns AS (SELECT
    Inning,
    CONCAT(inning_topbot,inning) AS Inninghalf,
    SUM((post_bat_score - bat_score)) AS runsScored
FROM 
    `valuesheet.MLB.hitting_data`
WHERE
    (post_bat_score - bat_score) NOT IN (0)
GROUP BY 
    Inning,
    Inninghalf
ORDER BY 
    Inning)

SELECT 
    Inning,
    Inninghalf,
    runsScored,
    SUM(runsScored) OVER (PARTITION BY inning) AS inningruns,
    decround((runsScored/(SELECT SUM(runsScored) FROM rawruns))*100) AS pctrunshalf,
    decround((SUM(runsScored) OVER (PARTITION BY inning))/(SELECT SUM(runsScored) FROM rawruns)*100) AS pctrunsinning,
FROM 
    rawruns
ORDER BY
    Inning