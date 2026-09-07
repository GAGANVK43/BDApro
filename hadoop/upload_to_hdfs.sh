#!/usr/bin/env bash
# ==========================================================
# upload_to_hdfs.sh - HDFS Dataset Ingestion Script (Linux/Mac/WSL)
# Creates HDFS directory structure and uploads raw & cleaned datasets
# ==========================================================

set -e

HDFS_BASE="/netflix-analytics"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=================================================="
echo "HADOOP HDFS INGESTION: NETFLIX BIG DATA PLATFORM"
echo "=================================================="

# Check if HDFS command exists
if ! command -v hdfs &> /dev/null; then
    echo "[!] Error: 'hdfs' command not found in PATH."
    echo "[!] Ensure Hadoop is installed and HADOOP_HOME/bin is on PATH."
    exit 1
fi

echo "[*] 1. Creating HDFS directory structure..."
hdfs dfs -mkdir -p ${HDFS_BASE}/raw
hdfs dfs -mkdir -p ${HDFS_BASE}/cleaned
hdfs dfs -mkdir -p ${HDFS_BASE}/output

echo "[✓] Created directories:"
echo "    - ${HDFS_BASE}/raw"
echo "    - ${HDFS_BASE}/cleaned"
echo "    - ${HDFS_BASE}/output"

echo ""
echo "[*] 2. Uploading raw dataset to HDFS..."
if [ -f "${PROJECT_DIR}/data/raw/netflix_titles.csv" ]; then
    hdfs dfs -put -f "${PROJECT_DIR}/data/raw/netflix_titles.csv" ${HDFS_BASE}/raw/
    echo "[✓] Raw dataset uploaded to ${HDFS_BASE}/raw/netflix_titles.csv"
fi

echo ""
echo "[*] 3. Uploading cleaned dataset to HDFS..."
if [ -f "${PROJECT_DIR}/data/cleaned/netflix_cleaned.csv" ]; then
    hdfs dfs -put -f "${PROJECT_DIR}/data/cleaned/netflix_cleaned.csv" ${HDFS_BASE}/cleaned/
    echo "[✓] Cleaned dataset uploaded to ${HDFS_BASE}/cleaned/netflix_cleaned.csv"
else
    echo "[!] Warning: Cleaned dataset not found locally. Run 'python python/data_cleaning.py' first."
fi

echo ""
echo "[*] 4. Verifying files in HDFS..."
hdfs dfs -ls -R ${HDFS_BASE}

echo "=================================================="
echo "[✓] HDFS Upload Completed Successfully!"
echo "=================================================="
