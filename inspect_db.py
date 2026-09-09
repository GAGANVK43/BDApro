"""
inspect_db.py - Interactive Command Prompt MongoDB Database Inspector
Usage: python inspect_db.py
"""

import sys
from pathlib import Path

# Add root directory to python path
sys.path.append(str(Path(__file__).resolve().parent))

from python.mongodb_connection import connect_mongodb


def inspect_database():
    print("=" * 65)
    print("      NETFLIX BIG DATA ANALYTICS: MONGODB DATABASE INSPECTOR")
    print("=" * 65)

    print("[*] Connecting to MongoDB Atlas Cloud Cluster...")
    db, client, error = connect_mongodb()

    if error or db is None:
        print(f"[!] Connection Error: {error}")
        print("=" * 65)
        return

    print("[OK] Connected successfully to Database:", db.name)
    print("=" * 65)

    # 1. List Collections & Document Counts
    collections = db.list_collection_names()
    print("\n--- ALL COLLECTIONS IN DATABASE ---")
    total_docs = 0
    for col_name in sorted(collections):
        count = db[col_name].count_documents({})
        total_docs += count
        print(f"  * {col_name:<22} : {count:>4} documents")
    print(f"  -------------------------------------")
    print(f"  TOTAL DOCUMENTS        : {total_docs:>4} documents\n")

    # 2. Show Summary KPIs
    summary = db.dashboard_summary.find_one({}, {"_id": 0})
    if summary:
        print("--- DASHBOARD SUMMARY METRICS ---")
        for k, v in summary.items():
            print(f"  {k:<24}: {v}")
        print()

    # 3. Sample Indian Titles
    print("--- SAMPLE INDIAN TITLES IN MONGODB (movies collection) ---")
    cursor = db.movies.find({"country": "India"}, {"_id": 0, "show_id": 1, "title": 1, "release_year": 1, "type": 1, "rating": 1, "genres": 1}).limit(8)
    for m in cursor:
        genres = ", ".join(m.get("genres", []))
        print(f"  [{m.get('show_id')}] {m.get('title')} ({m.get('release_year')}) | {m.get('type')} | Rating: {m.get('rating')} | Genres: {genres}")

    # 4. Top Producing Countries
    print("\n--- TOP CONTENT PRODUCING COUNTRIES ---")
    countries = db.country_statistics.find({}, {"_id": 0}).sort("count", -1).limit(5)
    for c in countries:
        print(f"  * {c.get('country'):<18} : {c.get('count'):>3} titles ({c.get('movies')} Movies, {c.get('tv_shows')} TV Shows)")

    print("=" * 65)
    client.close()


if __name__ == "__main__":
    inspect_database()
