"""
main.py - Master Application Entry Point
Launches the Flask Web Application & REST API for local execution.

Usage:
    python main.py
    python run.py
    python app.py
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from app import app, initialize_dataset
from python.utils import get_full_system_status


def print_banner():
    print("=" * 65)
    print("NETFLIX & MOVIE BIG DATA ANALYTICS PLATFORM")
    print("   Architecture: Python | Flask | MongoDB Atlas | Hadoop HDFS | Apache Hive")
    print("=" * 65)


def print_system_summary():
    """Prints a quick infrastructure health check."""
    status = get_full_system_status()
    print("\n--- System Infrastructure Status ---")
    print(f"[*] Python:   {status['python']['status']}")
    print(f"[*] Hadoop:   {status['hadoop']['status']}")
    print(f"[*] HDFS:     {status['hdfs']['status']}")
    print(f"[*] Hive:     {status['hive']['status']}")
    print(f"[*] MongoDB:  {status['mongodb']['status']}")
    print(f"[*] Dataset:  {status['dataset']['status']}")
    print("-------------------------------------\n")


if __name__ == "__main__":
    print_banner()
    initialize_dataset()
    print_system_summary()
    
    port = int(os.getenv("PORT", 5000))
    print(f"[*] Starting Flask Web Server at: http://127.0.0.1:{port}")
    print("[*] Press Ctrl+C to stop server.\n")
    app.run(host="0.0.0.0", port=port, debug=True)
