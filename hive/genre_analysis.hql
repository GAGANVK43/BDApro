-- ==========================================================
-- Apache Hive Query: Genre Analytics & Distribution
-- Uses LATERAL VIEW explode() to break multi-valued comma strings
-- ==========================================================

USE netflix_db;

-- 1. Overall Genre Frequency Analysis
SELECT 
    TRIM(genre_item) AS genre,
    COUNT(*) AS total_count,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_count,
    ROUND(AVG(rating_score), 2) AS avg_rating_score
FROM movies_orc
LATERAL VIEW explode(split(listed_in, ',')) exploded_table AS genre_item
WHERE TRIM(genre_item) != ''
GROUP BY TRIM(genre_item)
ORDER BY total_count DESC
LIMIT 20;

-- 2. Genre Trends by Year
SELECT 
    release_year,
    TRIM(genre_item) AS genre,
    COUNT(*) AS count_in_year
FROM movies_orc
LATERAL VIEW explode(split(listed_in, ',')) exploded_table AS genre_item
WHERE release_year >= 2015 AND TRIM(genre_item) != ''
GROUP BY release_year, TRIM(genre_item)
ORDER BY release_year DESC, count_in_year DESC;
