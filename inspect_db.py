"""
inspect_db.py - Comprehensive MongoDB Database Content Inspector
Usage:
    python inspect_db.py                 # Shows summary + samples from all collections
    python inspect_db.py all             # Shows full contents of all collections
    python inspect_db.py movies          # Shows documents in 'movies'
    python inspect_db.py genres          # Shows contents of 'genre_statistics'
    python inspect_db.py countries       # Shows contents of 'country_statistics'
    python inspect_db.py releases        # Shows contents of 'release_statistics'
    python inspect_db.py ratings         # Shows contents of 'rating_statistics'
    python inspect_db.py summary         # Shows contents of 'dashboard_summary'
"""

import sys
import pprint
from pathlib import Path

# Add root directory to python path
sys.path.append(str(Path(__file__).resolve().parent))

from python.mongodb_connection import connect_mongodb


def show_movies(db, limit=15):
    print("\n" + "=" * 80)
    print(f"📁 COLLECTION: 'movies' (Total: {db.movies.count_documents({})} documents)")
    print("=" * 80)
    cursor = db.movies.find({}, {"_id": 0}).limit(limit)
    for i, m in enumerate(cursor, 1):
        genres = ", ".join(m.get("genres", []))
        countries = ", ".join(m.get("country", []))
        print(f"[{i:02d}] ID: {m.get('show_id'):<5} | {m.get('title')} ({m.get('release_year')})")
        print(f"     Type: {m.get('type'):<8} | Rating: {m.get('rating'):<6} | Score: {m.get('rating_score')} | Duration: {m.get('duration')}")
        print(f"     Director: {m.get('director')}")
        print(f"     Cast    : {m.get('cast')[:80]}...")
        print(f"     Country : {countries}")
        print(f"     Genres  : {genres}")
        print(f"     Synopsis: {m.get('description')[:100]}...")
        print("-" * 80)
    if db.movies.count_documents({}) > limit:
        print(f"  ... and {db.movies.count_documents({}) - limit} more movie documents in MongoDB.")


def show_genre_statistics(db):
    print("\n" + "=" * 80)
    print(f"📁 COLLECTION: 'genre_statistics' ({db.genre_statistics.count_documents({})} genres)")
    print("=" * 80)
    print(f"{'#':<3} {'Genre Name':<30} {'Total Titles':<15} {'Movies':<10} {'TV Shows':<10}")
    print("-" * 80)
    cursor = db.genre_statistics.find({}, {"_id": 0}).sort("count", -1)
    for i, g in enumerate(cursor, 1):
        print(f"{i:<3} {g.get('genre'):<30} {g.get('count'):<15} {g.get('movies'):<10} {g.get('tv_shows'):<10}")


def show_country_statistics(db):
    print("\n" + "=" * 80)
    print(f"📁 COLLECTION: 'country_statistics' ({db.country_statistics.count_documents({})} countries)")
    print("=" * 80)
    print(f"{'#':<3} {'Country':<25} {'Total Titles':<15} {'Movies':<10} {'TV Shows':<10}")
    print("-" * 80)
    cursor = db.country_statistics.find({}, {"_id": 0}).sort("count", -1)
    for i, c in enumerate(cursor, 1):
        print(f"{i:<3} {c.get('country'):<25} {c.get('count'):<15} {c.get('movies'):<10} {c.get('tv_shows'):<10}")


def show_release_statistics(db):
    print("\n" + "=" * 80)
    print(f"📁 COLLECTION: 'release_statistics' ({db.release_statistics.count_documents({})} years)")
    print("=" * 80)
    print(f"{'Release Year':<15} {'Total Titles Added':<20} {'Movies':<12} {'TV Shows':<12}")
    print("-" * 80)
    cursor = db.release_statistics.find({}, {"_id": 0}).sort("release_year", 1)
    for r in cursor:
        print(f"{r.get('release_year'):<15} {r.get('count'):<20} {r.get('movies'):<12} {r.get('tv_shows'):<12}")


def show_rating_statistics(db):
    print("\n" + "=" * 80)
    print(f"📁 COLLECTION: 'rating_statistics' ({db.rating_statistics.count_documents({})} maturity ratings)")
    print("=" * 80)
    print(f"{'Maturity Rating':<20} {'Total Titles':<15} {'Movies':<12} {'TV Shows':<12}")
    print("-" * 80)
    cursor = db.rating_statistics.find({}, {"_id": 0}).sort("count", -1)
    for r in cursor:
        print(f"{r.get('rating'):<20} {r.get('count'):<15} {r.get('movies'):<12} {r.get('tv_shows'):<12}")


def show_dashboard_summary(db):
    print("\n" + "=" * 80)
    print("📁 COLLECTION: 'dashboard_summary' (Aggregated KPI Document)")
    print("=" * 80)
    summary = db.dashboard_summary.find_one({}, {"_id": 0})
    if summary:
        for k, v in summary.items():
            print(f"  * {k:<25} : {v}")


def inspect_database():
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    print("=" * 80)
    print("       NETFLIX BIG DATA ANALYTICS - MONGODB CONTENT INSPECTOR")
    print("=" * 80)
    print("[*] Connecting to MongoDB Atlas Cloud Cluster...")
    db, client, error = connect_mongodb()

    if error or db is None:
        print(f"[!] MongoDB Connection Error: {error}")
        print("=" * 80)
        return

    print(f"[OK] Connected to Database: '{db.name}'\n")

    if arg in ["all"]:
        show_dashboard_summary(db)
        show_country_statistics(db)
        show_genre_statistics(db)
        show_rating_statistics(db)
        show_release_statistics(db)
        show_movies(db, limit=10)
    elif arg in ["movies", "movie"]:
        show_movies(db, limit=30)
    elif arg in ["genres", "genre", "genre_statistics"]:
        show_genre_statistics(db)
    elif arg in ["countries", "country", "country_statistics"]:
        show_country_statistics(db)
    elif arg in ["releases", "release", "release_statistics", "years"]:
        show_release_statistics(db)
    elif arg in ["ratings", "rating", "rating_statistics"]:
        show_rating_statistics(db)
    elif arg in ["summary", "dashboard_summary"]:
        show_dashboard_summary(db)
    else:
        print(f"[!] Unknown collection filter: '{arg}'.")
        print("Available options: movies | genres | countries | releases | ratings | summary | all")

    print("\n" + "=" * 80)
    client.close()


if __name__ == "__main__":
    inspect_database()
