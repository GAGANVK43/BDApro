-- ==========================================================
-- Apache Hive Master Analytics Suite: complete_analysis.hql
-- Executes the complete analytics pipeline and generates analytical tables
-- ==========================================================

USE netflix_db;

-- 1. Table for Genre Summary
DROP TABLE IF EXISTS analytics_genre_summary;
CREATE TABLE analytics_genre_summary STORED AS ORC AS
SELECT 
    TRIM(genre_item) AS genre,
    COUNT(*) AS total_count,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_count,
    ROUND(AVG(rating_score), 2) AS avg_rating
FROM movies_orc
LATERAL VIEW explode(split(listed_in, ',')) exploded_table AS genre_item
WHERE TRIM(genre_item) != ''
GROUP BY TRIM(genre_item);

-- 2. Table for Rating Summary
DROP TABLE IF EXISTS analytics_rating_summary;
CREATE TABLE analytics_rating_summary STORED AS ORC AS
SELECT 
    rating,
    COUNT(*) AS total_count,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_count
FROM movies_orc
GROUP BY rating;

-- 3. Table for Release Year Summary
DROP TABLE IF EXISTS analytics_release_summary;
CREATE TABLE analytics_release_summary STORED AS ORC AS
SELECT 
    release_year,
    COUNT(*) AS total_count,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_count
FROM movies_orc
GROUP BY release_year;

-- 4. Table for Country Summary
DROP TABLE IF EXISTS analytics_country_summary;
CREATE TABLE analytics_country_summary STORED AS ORC AS
SELECT 
    TRIM(country_item) AS country,
    COUNT(*) AS total_count,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_show_count
FROM movies_orc
LATERAL VIEW explode(split(country, ',')) exploded_table AS country_item
WHERE TRIM(country_item) != '' AND TRIM(country_item) != 'Unknown'
GROUP BY TRIM(country_item);

-- 5. Export Summary Metrics to HDFS
INSERT OVERWRITE DIRECTORY '/netflix-analytics/output/summary'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 
    COUNT(*) AS total_records,
    SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS total_movies,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS total_tv_shows,
    COUNT(DISTINCT release_year) AS total_years
FROM movies_orc;
