"""
run.py - Alias launcher for main.py (Flask Web Application)
"""

from main import print_banner, initialize_dataset, print_system_summary
from app import app
import os

if __name__ == "__main__":
    print_banner()
    initialize_dataset()
    print_system_summary()
    
    port = int(os.getenv("PORT", 5000))
    print(f"[*] Starting Flask Web Server at: http://127.0.0.1:{port}")
    print("[*] Press Ctrl+C to stop server.\n")
    app.run(host="0.0.0.0", port=port, debug=True)
