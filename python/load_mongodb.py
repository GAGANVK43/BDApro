"""
load_mongodb.py - MongoDB Atlas / Local Ingestion Pipeline
Loads cleaned Netflix dataset and pre-calculated aggregations into MongoDB collections:
- movies (with rich schema, array types for genres and countries)
- genre_statistics
- rating_statistics
- release_statistics
- country_statistics
- dashboard_summary

Creates optimized indexes for rapid query performance.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Ensure root directory is on path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from python.mongodb_connection import connect_mongodb
from python.data_cleaning import clean_dataset, load_dataset, save_cleaned_data, find_raw_dataset

CLEANED_CSV_PATH = BASE_DIR / "data" / "cleaned" / "netflix_cleaned.csv"


def prepare_movie_documents(df: pd.DataFrame) -> list[dict]:
    """Converts Pandas DataFrame into MongoDB document format."""
    documents = []
    for _, row in df.iterrows():
        # Parse genres as array
        raw_genres = str(row.get("listed_in", ""))
        genres = [g.strip() for g in raw_genres.split(",") if g.strip()] if raw_genres else ["General"]

        # Parse countries as array
        raw_countries = str(row.get("country", ""))
        countries = [c.strip() for c in raw_countries.split(",") if c.strip() and c != "Unknown"]
        if not countries:
            countries = ["Unknown"]

        doc = {
            "show_id": str(row.get("show_id", "")),
            "type": str(row.get("type", "Movie")),
            "title": str(row.get("title", "")),
            "director": str(row.get("director", "Unknown Director")),
            "cast": str(row.get("cast", "Unknown Cast")),
            "country": countries,
            "primary_country": str(row.get("primary_country", "Unknown")),
            "release_year": int(row.get("release_year", 2020)),
            "rating": str(row.get("rating", "TV-MA")),
            "rating_score": float(row.get("rating_score", 7.5)),
            "duration": str(row.get("duration", "")),
            "duration_numeric": int(row.get("duration_numeric", 0)),
            "duration_unit": str(row.get("duration_unit", "Minutes")),
            "genres": genres,
            "primary_genre": str(row.get("primary_genre", "General")),
            "description": str(row.get("description", "")),
            "added_year": int(row.get("added_year", row.get("release_year", 2020))),
            "added_month": str(row.get("added_month", "Unknown"))
        }
        documents.append(doc)
    return documents


def generate_statistics_collections(df: pd.DataFrame) -> dict:
    """Computes aggregation statistics collections ready for MongoDB insertion."""
    stats = {}

    # 1. Genre Statistics
    genre_rows = []
    for _, row in df.iterrows():
        genres = [g.strip() for g in str(row["listed_in"]).split(",") if g.strip()]
        for g in genres:
            genre_rows.append({"genre": g, "type": row["type"]})
    gdf = pd.DataFrame(genre_rows)
    if not gdf.empty:
        genre_summary = gdf.groupby("genre").agg(
            count=("type", "count"),
            movies=("type", lambda s: (s == "Movie").sum()),
            tv_shows=("type", lambda s: (s == "TV Show").sum())
        ).reset_index().sort_values(by="count", ascending=False)
        stats["genre_statistics"] = genre_summary.to_dict(orient="records")
    else:
        stats["genre_statistics"] = []

    # 2. Rating Statistics
    rating_summary = df.groupby("rating").agg(
        count=("show_id", "count"),
        movies=("type", lambda s: (s == "Movie").sum()),
        tv_shows=("type", lambda s: (s == "TV Show").sum())
    ).reset_index().sort_values(by="count", ascending=False)
    stats["rating_statistics"] = rating_summary.to_dict(orient="records")

    # 3. Release Year Statistics
    release_summary = df.groupby("release_year").agg(
        count=("show_id", "count"),
        movies=("type", lambda s: (s == "Movie").sum()),
        tv_shows=("type", lambda s: (s == "TV Show").sum())
    ).reset_index().sort_values(by="release_year", ascending=True)
    stats["release_statistics"] = release_summary.to_dict(orient="records")

    # 4. Country Statistics
    country_rows = []
    for _, row in df.iterrows():
        countries = [c.strip() for c in str(row["country"]).split(",") if c.strip() and c != "Unknown"]
        for c in countries:
            country_rows.append({"country": c, "type": row["type"]})
    cdf = pd.DataFrame(country_rows)
    if not cdf.empty:
        country_summary = cdf.groupby("country").agg(
            count=("type", "count"),
            movies=("type", lambda s: (s == "Movie").sum()),
            tv_shows=("type", lambda s: (s == "TV Show").sum())
        ).reset_index().sort_values(by="count", ascending=False)
        stats["country_statistics"] = country_summary.to_dict(orient="records")
    else:
        stats["country_statistics"] = []

    # 5. Dashboard Summary
    stats["dashboard_summary"] = [{
        "total_content": len(df),
        "total_movies": int((df["type"] == "Movie").sum()),
        "total_tv_shows": int((df["type"] == "TV Show").sum()),
        "unique_genres": int(len(stats["genre_statistics"])),
        "unique_countries": int(len(stats["country_statistics"])),
        "average_rating_score": round(float(df["rating_score"].mean()), 2) if "rating_score" in df else 7.5,
        "earliest_year": int(df["release_year"].min()),
        "latest_year": int(df["release_year"].max())
    }]

    return stats


def load_data_to_mongodb():
    """Main ingestion pipeline to push dataset and stats to MongoDB."""
    print("=" * 60)
    print("NETFLIX BIG DATA ANALYTICS: MONGODB INGESTION PIPELINE")
    print("=" * 60)

    # 1. Check/create cleaned dataset
    if not CLEANED_CSV_PATH.exists():
        print("[*] Cleaned CSV not found. Running data cleaning pipeline first...")
        raw_path = find_raw_dataset()
        df_raw = load_dataset(raw_path)
        df_cleaned, _ = clean_dataset(df_raw)
        save_cleaned_data(df_cleaned)
    else:
        df_cleaned = pd.read_csv(CLEANED_CSV_PATH)

    print(f"[*] Prepared {len(df_cleaned)} cleaned movie records.")

    # 2. Connect to MongoDB
    print("[*] Connecting to MongoDB...")
    db, client, error = connect_mongodb()

    if error or db is None:
        print(f"[!] MongoDB Connection Failed: {error}")
        print("[!] Note: The dashboard will gracefully fallback to local cleaned data.")
        print("[!] To connect MongoDB Atlas, set MONGODB_URI in config/.env file.")
        print("=" * 60)
        return False

    try:
        # 3. Ingest movies collection
        movie_docs = prepare_movie_documents(df_cleaned)
        movies_col = db["movies"]
        movies_col.drop()  # Clean refresh for idempotency
        movies_col.insert_many(movie_docs)
        print(f"[OK] Inserted {len(movie_docs)} documents into 'movies' collection.")

        # Create indexes
        movies_col.create_index("show_id", unique=True)
        movies_col.create_index("title")
        movies_col.create_index("release_year")
        movies_col.create_index("type")
        movies_col.create_index("rating")
        movies_col.create_index("genres")
        movies_col.create_index("country")
        print("[OK] Created indexes on title, release_year, type, rating, genres, country.")

        # 4. Ingest Aggregation Statistics Collections
        stats = generate_statistics_collections(df_cleaned)
        for col_name, data in stats.items():
            col = db[col_name]
            col.drop()
            if data:
                col.insert_many(data)
            print(f"[OK] Populated '{col_name}' collection ({len(data)} records).")

        print("=" * 60)
        print("[OK] MongoDB Ingestion Pipeline Completed Successfully!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"[!] Error inserting data into MongoDB: {str(e)}")
        return False
    finally:
        client.close()


if __name__ == "__main__":
    load_data_to_mongodb()
