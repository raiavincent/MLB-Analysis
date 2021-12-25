-- Declare vars
--  Don't want the 4 seam at a certain point in this query

DECLARE seam4 STRING DEFAULT 'FF';

-- Temp function to get year

CREATE TEMP FUNCTION getYear(x DATE)
    RETURNS INT64
    AS (EXTRACT(year FROM x));

--Get chapman's fastest pitches grouped by pitch and year

WITH pitches AS (SELECT
    getYear(gd.game_date) AS year,
    max(pv.release_speed) AS fastest_pitch,
    pv.pitch_type
FROM
    `valuesheet.MLB.pitching_view` AS pv
LEFT JOIN 
    `valuesheet.MLB.game_data` AS gd ON pv.game_pk = gd.game_pk
WHERE 
    pv.pitcher_full = "Aroldis Chapman"
    AND pv.pitch_type NOT IN (seam4)
GROUP BY
    year,
    pv.pitch_type
ORDER BY
    fastest_pitch DESC
),

-- Rank his fastest pitches by pitch

pitchrank AS (SELECT 
    year,
    pitch_type,
    fastest_pitch,
    RANK() OVER(PARTITION BY pitch_type ORDER BY fastest_pitch DESC) AS Rank
FROM
    pitches
ORDER BY 
    fastest_pitch DESC,
    Rank),

-- Rank his fastest pitches by year

yearrank AS (SELECT
    year,
    fastest_pitch,
    pitch_type,
    RANK() OVER(PARTITION BY year ORDER BY fastest_pitch DESC) AS rankyear
FROM 
    pitchrank
ORDER BY
    rankyear)

-- Select the best 1 rank pitches by year

SELECT
    yr.year,
    yr.fastest_pitch,
    pr.pitch_name
FROM 
    yearrank AS yr
LEFT JOIN 
    `valuesheet.MLB.pitch_ref` AS pr ON yr.pitch_type = pr.pitch_type
WHERE 
    rankyear = 1
ORDER BY 
    fastest_pitch DESC