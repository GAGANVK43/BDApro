"""
utils.py - Big Data Infrastructure Health & Utility Helpers
Provides connection checking for Hadoop, HDFS, Apache Hive, MongoDB, and local datasets.
"""

import os
import shutil
import subprocess
import socket
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
CLEANED_DATA_DIR = BASE_DIR / "data" / "cleaned"


def check_hadoop_status():
    """
    Checks if Hadoop binaries are installed and accessible on PATH or configured in HADOOP_HOME.
    Also verifies HDFS accessibility.
    """
    hadoop_home = os.getenv("HADOOP_HOME")
    hadoop_cmd = shutil.which("hadoop") or (os.path.join(hadoop_home, "bin", "hadoop") if hadoop_home else None)
    
    if hadoop_cmd and os.path.exists(hadoop_cmd if not shutil.which("hadoop") else hadoop_cmd):
        try:
            # Test Hadoop command
            res = subprocess.run([hadoop_cmd, "version"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                first_line = res.stdout.strip().split("\n")[0] if res.stdout else "Hadoop Available"
                return {
                    "installed": True,
                    "running": True,
                    "version": first_line,
                    "status": "RUNNING / AVAILABLE",
                    "details": f"Detected Hadoop at {hadoop_cmd}"
                }
        except Exception as e:
            return {
                "installed": True,
                "running": False,
                "version": "Unknown",
                "status": "NOT RUNNING",
                "details": f"Hadoop found but command failed: {str(e)}"
            }
    
    return {
        "installed": False,
        "running": False,
        "version": None,
        "status": "NOT AVAILABLE",
        "details": "Hadoop binaries not detected on PATH or HADOOP_HOME."
    }


def check_hdfs_status():
    """
    Verifies if HDFS NameNode / DataNode is active and responsive.
    """
    hdfs_cmd = shutil.which("hdfs")
    if hdfs_cmd:
        try:
            res = subprocess.run([hdfs_cmd, "dfsadmin", "-report"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                return {
                    "available": True,
                    "status": "AVAILABLE / ACTIVE",
                    "details": "HDFS cluster report responded successfully."
                }
        except Exception as e:
            return {
                "available": False,
                "status": "NOT AVAILABLE",
                "details": f"HDFS command error: {str(e)}"
            }
            
    # Fallback: check typical NameNode port 9000 / 9870
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.5)
    try:
        result = sock.connect_ex(('127.0.0.1', 9000))
        if result == 0:
            return {"available": True, "status": "AVAILABLE", "details": "NameNode port 9000 responding."}
    except Exception:
        pass
    finally:
        sock.close()

    return {
        "available": False,
        "status": "NOT AVAILABLE",
        "details": "HDFS service is not running or unreachable on default ports."
    }


def check_hive_status():
    """
    Checks if Apache Hive (hive or beeline) CLI is installed and available.
    """
    hive_home = os.getenv("HIVE_HOME")
    hive_cmd = shutil.which("hive") or (os.path.join(hive_home, "bin", "hive") if hive_home else None)
    
    if hive_cmd and os.path.exists(hive_cmd if not shutil.which("hive") else hive_cmd):
        try:
            res = subprocess.run([hive_cmd, "--version"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                first_line = res.stdout.strip().split("\n")[0] if res.stdout else "Hive Available"
                return {
                    "installed": True,
                    "status": "AVAILABLE / READY",
                    "version": first_line,
                    "details": f"Hive executable detected at {hive_cmd}"
                }
        except Exception as e:
            return {
                "installed": True,
                "status": "INSTALLED (OFFLINE)",
                "version": "Unknown",
                "details": f"Hive command error: {str(e)}"
            }

    return {
        "installed": False,
        "status": "NOT AVAILABLE",
        "version": None,
        "details": "Apache Hive binaries not detected on PATH or HIVE_HOME."
    }


def check_dataset_status():
    """
    Checks raw and cleaned dataset presence and size.
    """
    raw_files = list(RAW_DATA_DIR.glob("*.csv")) if RAW_DATA_DIR.exists() else []
    cleaned_file = CLEANED_DATA_DIR / "netflix_cleaned.csv"
    
    has_raw = len(raw_files) > 0
    has_cleaned = cleaned_file.exists() and cleaned_file.stat().st_size > 0
    
    return {
        "raw_present": has_raw,
        "raw_files": [f.name for f in raw_files],
        "cleaned_present": has_cleaned,
        "cleaned_path": str(cleaned_file) if has_cleaned else None,
        "status": "LOADED / READY" if (has_raw or has_cleaned) else "NOT FOUND"
    }


def get_full_system_status():
    """
    Aggregates health checks across all components:
    Python, Hadoop, HDFS, Hive, MongoDB, and Datasets.
    """
    # MongoDB status import
    from python.mongodb_connection import check_mongodb_status
    
    return {
        "python": {
            "status": "CONNECTED / READY",
            "version": f"Python {os.sys.version.split()[0]}",
            "details": "Python execution environment is active and running."
        },
        "hadoop": check_hadoop_status(),
        "hdfs": check_hdfs_status(),
        "hive": check_hive_status(),
        "mongodb": check_mongodb_status(),
        "dataset": check_dataset_status()
    }
