"""
pipeline_service.py - Big Data Pipeline & Infrastructure Monitoring Service
Handles real-time health checks for Python, Hadoop HDFS, Apache Hive, MongoDB, and Datasets.
"""

from pathlib import Path
from python.utils import get_full_system_status
from python.data_cleaning import clean_dataset, load_dataset, save_cleaned_data, find_raw_dataset, RAW_DIR, CLEANED_DIR
from python.load_mongodb import load_data_to_mongodb
import pandas as pd


def get_pipeline_health() -> dict:
    """Returns real status of all Big Data platform components."""
    return get_full_system_status()


def trigger_data_cleaning() -> dict:
    """Executes the Python data cleaning pipeline."""
    try:
        raw_path = find_raw_dataset()
        df_raw = load_dataset(raw_path)
        cleaned_df, metrics = clean_dataset(df_raw)
        out_path = save_cleaned_data(cleaned_df)
        
        return {
            "success": True,
            "message": "Data cleaning executed successfully.",
            "metrics": metrics,
            "output_file": str(out_path.name)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error during data cleaning: {str(e)}"
        }


def trigger_mongodb_sync() -> dict:
    """Triggers dataset ingestion into MongoDB Atlas."""
    try:
        success = load_data_to_mongodb()
        if success:
            return {
                "success": True,
                "message": "Successfully ingested cleaned dataset and aggregations into MongoDB Atlas."
            }
        else:
            return {
                "success": False,
                "message": "MongoDB is not connected. Configure MONGODB_URI in environment."
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error ingesting into MongoDB: {str(e)}"
        }
