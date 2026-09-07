-- ==========================================================
-- Apache Hive Query: Rating Distribution & Maturity Classification
-- Aggregates ratings by content type and proportions
-- ==========================================================

USE netflix_db;

-- 1. Rating Distribution with Proportions
SELECT 
    rating,
    COUNT(*) AS total_titles,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage_of_catalog,
    ROUND(AVG(rating_score), 2) AS avg_quality_score
FROM movies_orc
WHERE rating IS NOT NULL AND rating != ''
GROUP BY rating
ORDER BY total_titles DESC;

-- 2. Top-Rated Content Breakdown
SELECT 
    title,
    type,
    release_year,
    rating,
    rating_score,
    primary_genre,
    primary_country
FROM movies_orc
ORDER BY rating_score DESC, release_year DESC
LIMIT 15;
