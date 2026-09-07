-- ==========================================================
-- Apache Hive Query: Geographic & Country-Wise Content Distribution
-- Breaks multi-country co-productions using LATERAL VIEW explode()
-- ==========================================================

USE netflix_db;

-- 1. Top 15 Content-Producing Countries
SELECT 
    TRIM(country_item) AS country,
    COUNT(*) AS total_productions,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_productions,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_productions,
    ROUND(AVG(rating_score), 2) AS avg_country_score
FROM movies_orc
LATERAL VIEW explode(split(country, ',')) exploded_table AS country_item
WHERE TRIM(country_item) != '' AND TRIM(country_item) != 'Unknown'
GROUP BY TRIM(country_item)
ORDER BY total_productions DESC
LIMIT 15;

-- 2. Country-Genre Matrix (Top genres for United States, India, UK, Japan, South Korea)
SELECT 
    TRIM(country_item) AS country,
    primary_genre,
    COUNT(*) AS title_count
FROM movies_orc
LATERAL VIEW explode(split(country, ',')) exploded_table AS country_item
WHERE TRIM(country_item) IN ('United States', 'India', 'United Kingdom', 'Japan', 'South Korea')
GROUP BY TRIM(country_item), primary_genre
ORDER BY country ASC, title_count DESC;
