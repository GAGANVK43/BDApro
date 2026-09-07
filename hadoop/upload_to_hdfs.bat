@echo off
rem ==========================================================
rem upload_to_hdfs.bat - HDFS Dataset Ingestion Script (Windows)
rem ==========================================================

echo ==================================================
echo HADOOP HDFS INGESTION: NETFLIX BIG DATA PLATFORM
echo ==================================================

set HDFS_BASE=/netflix-analytics

where hdfs >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] Error: 'hdfs' command not found.
    echo [!] Ensure Hadoop is installed and HADOOP_HOME\bin is on PATH.
    pause
    exit /b 1
)

echo [*] 1. Creating HDFS directories...
hdfs dfs -mkdir -p %HDFS_BASE%/raw
hdfs dfs -mkdir -p %HDFS_BASE%/cleaned
hdfs dfs -mkdir -p %HDFS_BASE%/output

echo [*] 2. Uploading raw dataset...
if exist "%~dp0..\data\raw\netflix_titles.csv" (
    hdfs dfs -put -f "%~dp0..\data\raw\netflix_titles.csv" %HDFS_BASE%/raw/
    echo [✓] Uploaded raw dataset.
)

echo [*] 3. Uploading cleaned dataset...
if exist "%~dp0..\data\cleaned\netflix_cleaned.csv" (
    hdfs dfs -put -f "%~dp0..\data\cleaned\netflix_cleaned.csv" %HDFS_BASE%/cleaned/
    echo [✓] Uploaded cleaned dataset.
) else (
    echo [!] Run 'python python\data_cleaning.py' first to generate cleaned dataset.
)

echo [*] 4. Verifying HDFS contents:
hdfs dfs -ls -R %HDFS_BASE%

echo ==================================================
echo [✓] HDFS Upload Completed!
echo ==================================================
