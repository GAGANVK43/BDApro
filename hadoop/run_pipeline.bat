@echo off
rem ==========================================================
rem run_pipeline.bat - End-to-End Big Data Orchestration (Windows)
rem ==========================================================

echo ==========================================================
echo NETFLIX BIG DATA PLATFORM: FULL PIPELINE ORCHESTRATION
echo ==========================================================

cd /d "%~dp0.."

echo.
echo [STEP 1/5] Running Python Data Cleaning Pipeline...
python python\data_cleaning.py

echo.
echo [STEP 2/5] Ingesting Cleaned Dataset into Hadoop HDFS...
call hadoop\upload_to_hdfs.bat

echo.
echo [STEP 3/5] Executing Apache Hive DDL & Table Partitioning...
hive -f hive\create_tables.hql

echo.
echo [STEP 4/5] Executing Hive Big Data Analytical Queries...
hive -f hive\complete_analysis.hql

echo.
echo [STEP 5/5] Ingesting Processed Data into MongoDB Collections...
python python\load_mongodb.py

echo.
echo ==========================================================
echo [✓] Pipeline execution finished!
echo     Run: python app.py to launch the Flask Web Dashboard
echo ==========================================================
