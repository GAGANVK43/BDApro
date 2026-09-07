-- ==========================================================
-- Apache Hive Query: Release Year Trends & Content Growth
-- Calculates yearly trends and Year-over-Year growth using window functions
-- ==========================================================

USE netflix_db;

-- 1. Yearly Content Production Breakdown
SELECT 
    release_year,
    COUNT(*) AS total_releases,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_releases,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_releases
FROM movies_orc
GROUP BY release_year
ORDER BY release_year ASC;

-- 2. Content Growth Velocity (YoY Growth Rate using LAG)
WITH yearly_counts AS (
    SELECT 
        release_year,
        COUNT(*) AS current_count
    FROM movies_orc
    GROUP BY release_year
)
SELECT 
    release_year,
    current_count,
    LAG(current_count, 1) OVER (ORDER BY release_year ASC) AS prev_year_count,
    ROUND(((current_count - LAG(current_count, 1) OVER (ORDER BY release_year ASC)) * 100.0) / 
          NULLIF(LAG(current_count, 1) OVER (ORDER BY release_year ASC), 0), 2) AS yoy_growth_percent
FROM yearly_counts
ORDER BY release_year ASC;
