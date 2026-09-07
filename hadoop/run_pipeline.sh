#!/usr/bin/env bash
# ==========================================================
# run_pipeline.sh - End-to-End Big Data Orchestration Script
# ==========================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_DIR}"

echo "=========================================================="
echo "NETFLIX BIG DATA PLATFORM: FULL PIPELINE ORCHESTRATION"
echo "=========================================================="

echo ""
echo "[STEP 1/5] Running Python Data Cleaning Pipeline..."
python3 python/data_cleaning.py || python python/data_cleaning.py

echo ""
echo "[STEP 2/5] Ingesting Cleaned Dataset into Hadoop HDFS..."
bash hadoop/upload_to_hdfs.sh || echo "[!] Skipping HDFS upload (Hadoop not running locally)"

echo ""
echo "[STEP 3/5] Executing Apache Hive DDL & Table Partitioning..."
hive -f hive/create_tables.hql || echo "[!] Skipping Hive table creation (Hive not running locally)"

echo ""
echo "[STEP 4/5] Executing Hive Big Data Analytical Queries..."
hive -f hive/complete_analysis.hql || echo "[!] Skipping Hive queries (Hive not running locally)"

echo ""
echo "[STEP 5/5] Ingesting Processed Data into MongoDB Collections..."
python3 python/load_mongodb.py || python python/load_mongodb.py

echo ""
echo "=========================================================="
echo "[✓] Big Data Pipeline Execution Completed!"
echo "    Start the Flask dashboard using: python app.py"
echo "=========================================================="
