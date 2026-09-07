-- ==========================================================
-- Apache Hive DDL: Netflix Movies & TV Shows Analytics Table
-- Creates database, external table over HDFS, and managed analytics tables
-- ==========================================================

CREATE DATABASE IF NOT EXISTS netflix_db
COMMENT 'Database for Netflix and Movie Big Data Analytics';

USE netflix_db;

-- 1. External Table pointing to cleaned dataset in HDFS
DROP TABLE IF EXISTS movies_raw_external;

CREATE EXTERNAL TABLE IF NOT EXISTS movies_raw_external (
    show_id STRING COMMENT 'Unique identifier for Movie/TV Show',
    type STRING COMMENT 'Type: Movie or TV Show',
    title STRING COMMENT 'Title of the title',
    director STRING COMMENT 'Director name',
    cast STRING COMMENT 'Cast members',
    country STRING COMMENT 'Production country list',
    primary_country STRING COMMENT 'Primary origin country',
    date_added STRING COMMENT 'Date added to platform',
    added_year INT COMMENT 'Year added',
    added_month STRING COMMENT 'Month added',
    release_year INT COMMENT 'Original release year',
    rating STRING COMMENT 'Maturity rating (e.g., PG-13, TV-MA)',
    rating_score DOUBLE COMMENT 'Normalized rating quality score',
    duration STRING COMMENT 'Full duration string',
    duration_numeric INT COMMENT 'Duration numeric value',
    duration_unit STRING COMMENT 'Minutes or Seasons',
    listed_in STRING COMMENT 'Comma-separated genres',
    primary_genre STRING COMMENT 'Primary genre category',
    description STRING COMMENT 'Synopsis/Plot overview'
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",",
   "quoteChar"     = "\"",
   "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/netflix-analytics/cleaned'
TBLPROPERTIES ("skip.header.line.count"="1");

-- 2. Partitioned ORC Table for Optimized Big Data Querying
DROP TABLE IF EXISTS movies_orc;

CREATE TABLE IF NOT EXISTS movies_orc (
    show_id STRING,
    title STRING,
    director STRING,
    cast STRING,
    country STRING,
    primary_country STRING,
    date_added STRING,
    added_year INT,
    added_month STRING,
    release_year INT,
    rating STRING,
    rating_score DOUBLE,
    duration STRING,
    duration_numeric INT,
    duration_unit STRING,
    listed_in STRING,
    primary_genre STRING,
    description STRING
)
PARTITIONED BY (type STRING)
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");

-- Load data from external table into partitioned ORC table
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

INSERT OVERWRITE TABLE movies_orc PARTITION(type)
SELECT 
    show_id,
    title,
    director,
    cast,
    country,
    primary_country,
    date_added,
    added_year,
    added_month,
    release_year,
    rating,
    rating_score,
    duration,
    duration_numeric,
    duration_unit,
    listed_in,
    primary_genre,
    description,
    type
FROM movies_raw_external
WHERE show_id IS NOT NULL AND show_id != 'show_id';
