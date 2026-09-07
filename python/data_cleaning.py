"""
data_cleaning.py - Big Data Ingestion & Preprocessing Pipeline
Cleans raw movie/Netflix dataset: deduplicates, normalizes types, imputes nulls,
parses durations, genres, and countries into standardized formats ready for HDFS, Hive, and MongoDB.
"""

import os
import re
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"


def find_raw_dataset() -> Path:
    """Finds the most suitable CSV in data/raw/ directory."""
    if not RAW_DIR.exists():
        RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    csv_files = list(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV dataset found in {RAW_DIR}")
    
    # Priority for netflix_titles.csv or first CSV found
    for f in csv_files:
        if "netflix" in f.name.lower():
            return f
    return csv_files[0]


def load_dataset(file_path: Path = None) -> pd.DataFrame:
    """Loads raw dataset into Pandas DataFrame."""
    target_path = file_path if file_path else find_raw_dataset()
    df = pd.read_csv(target_path, encoding="utf-8", low_memory=False)
    return df


def clean_duration(val: str, content_type: str) -> tuple[int, str]:
    """
    Parses duration string like '90 min' or '2 Seasons' into (numeric_value, unit).
    """
    if pd.isna(val) or not str(val).strip():
        return (0, "Unknown")
    
    val_str = str(val).strip()
    match = re.search(r'(\d+)', val_str)
    num = int(match.group(1)) if match else 0
    
    if "season" in val_str.lower():
        unit = "Seasons"
    elif "min" in val_str.lower():
        unit = "Minutes"
    else:
        unit = "Minutes" if content_type == "Movie" else "Seasons"
        
    return num, unit


def clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Main data cleaning pipeline.
    Returns:
        (cleaned_df, cleaning_metrics_dict)
    """
    initial_rows = len(df)
    metrics = {
        "initial_rows": initial_rows,
        "duplicates_removed": 0,
        "missing_imputed": {},
        "final_rows": 0
    }

    # 1. Normalize Column Names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Required core columns with fallbacks
    expected_cols = [
        "show_id", "type", "title", "director", "cast",
        "country", "date_added", "release_year", "rating",
        "duration", "listed_in", "description"
    ]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = "Unknown"

    # 2. Deduplication based on show_id or title
    df = df.drop_duplicates(subset=["title", "release_year"], keep="first")
    df = df.drop_duplicates(subset=["show_id"], keep="first")
    metrics["duplicates_removed"] = initial_rows - len(df)

    # 3. Clean and Normalize Content Type
    def normalize_type(t):
        if pd.isna(t):
            return "Movie"
        t_str = str(t).strip().lower()
        if "tv" in t_str or "show" in t_str or "series" in t_str:
            return "TV Show"
        return "Movie"

    df["type"] = df["type"].apply(normalize_type)

    # 4. Clean and Normalize Title
    df["title"] = df["title"].fillna("Untitled Content").astype(str).str.strip()

    # 5. Impute Missing Metadata (Director, Cast, Country)
    metrics["missing_imputed"]["director"] = int(df["director"].isna().sum())
    metrics["missing_imputed"]["cast"] = int(df["cast"].isna().sum())
    metrics["missing_imputed"]["country"] = int(df["country"].isna().sum())
    metrics["missing_imputed"]["rating"] = int(df["rating"].isna().sum())

    df["director"] = df["director"].fillna("Unknown Director").astype(str).str.strip()
    df["cast"] = df["cast"].fillna("Unknown Cast").astype(str).str.strip()
    df["country"] = df["country"].fillna("Unknown Country").astype(str).str.strip()
    
    # Clean up multi-country format (strip individual country elements)
    def clean_csv_field(text):
        if not text or text == "Unknown":
            return "Unknown"
        items = [i.strip() for i in str(text).split(",") if i.strip()]
        return ", ".join(items) if items else "Unknown"

    df["country"] = df["country"].apply(clean_csv_field)
    df["primary_country"] = df["country"].apply(lambda c: c.split(",")[0].strip() if c else "Unknown")

    # 6. Parse and Clean Release Year
    def clean_year(y):
        try:
            val = int(re.search(r'\d{4}', str(y)).group(0))
            if 1900 <= val <= 2030:
                return val
            return 2020
        except Exception:
            return 2020

    df["release_year"] = df["release_year"].apply(clean_year).astype(int)

    # 7. Parse date_added
    df["date_added"] = pd.to_datetime(df["date_added"].astype(str).str.strip(), errors="coerce")
    df["added_year"] = df["date_added"].dt.year.fillna(df["release_year"]).astype(int)
    df["added_month"] = df["date_added"].dt.strftime("%B").fillna("Unknown")

    # 8. Clean and Standardize Rating
    rating_map = {
        "UR": "NR",
        "UNRATED": "NR",
        "NOT RATED": "NR"
    }
    df["rating"] = df["rating"].fillna("TV-MA").astype(str).str.strip().str.upper()
    df["rating"] = df["rating"].replace(rating_map)
    # If rating contains numeric duration by mistake (rare raw netflix anomaly), fix it
    anomalous_mask = df["rating"].str.contains("MIN|SEASON", na=False, case=False)
    df.loc[anomalous_mask, "duration"] = df.loc[anomalous_mask, "rating"]
    df.loc[anomalous_mask, "rating"] = "TV-MA"

    # 9. Clean Duration into integer value and unit
    duration_parsed = [clean_duration(row["duration"], row["type"]) for _, row in df.iterrows()]
    df["duration_numeric"] = [dp[0] for dp in duration_parsed]
    df["duration_unit"] = [dp[1] for dp in duration_parsed]
    df["duration"] = [f"{dp[0]} {dp[1]}" for dp in duration_parsed]

    # 10. Clean and Normalize Listed_in (Genres)
    df["listed_in"] = df["listed_in"].fillna("General").astype(str).apply(clean_csv_field)
    df["primary_genre"] = df["listed_in"].apply(lambda g: g.split(",")[0].strip() if g else "General")

    # 11. Clean Description
    df["description"] = df["description"].fillna("No description available.").astype(str).str.strip()

    # 12. Synthetic normalized rating score for ranking analytics (e.g. 7.0 - 9.5 based on genre/year hash)
    def calculate_score(row):
        hash_val = (hash(str(row["title"]) + str(row["release_year"])) % 30) / 10.0
        return round(6.5 + hash_val, 1)

    df["rating_score"] = df.apply(calculate_score, axis=1)

    # 13. Reorder columns cleanly
    final_cols = [
        "show_id", "type", "title", "director", "cast",
        "country", "primary_country", "date_added", "added_year", "added_month",
        "release_year", "rating", "rating_score", "duration", "duration_numeric",
        "duration_unit", "listed_in", "primary_genre", "description"
    ]
    cleaned_df = df[final_cols].copy()
    metrics["final_rows"] = len(cleaned_df)

    return cleaned_df, metrics


def save_cleaned_data(df: pd.DataFrame) -> Path:
    """Saves cleaned DataFrame to data/cleaned/netflix_cleaned.csv."""
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CLEANED_DIR / "netflix_cleaned.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")
    return out_path


def run_data_cleaning_pipeline():
    """CLI execution entrypoint for data cleaning."""
    print("=" * 60)
    print("NETFLIX BIG DATA ANALYTICS: DATA CLEANING PIPELINE")
    print("=" * 60)
    
    try:
        raw_path = find_raw_dataset()
        print(f"[*] Found raw dataset at: {raw_path}")
        
        df_raw = load_dataset(raw_path)
        print(f"[*] Loaded {len(df_raw)} raw records.")
        
        cleaned_df, metrics = clean_dataset(df_raw)
        out_path = save_cleaned_data(cleaned_df)
        
        print(f"[OK] Cleaning completed successfully!")
        print(f"    - Raw Records: {metrics['initial_rows']}")
        print(f"    - Duplicates Removed: {metrics['duplicates_removed']}")
        print(f"    - Missing Values Handled: {metrics['missing_imputed']}")
        print(f"    - Cleaned Records Saved: {metrics['final_rows']}")
        print(f"    - Output: {out_path}")
        print("=" * 60)
        return cleaned_df, metrics
    except Exception as e:
        print(f"[ERROR] Error during cleaning: {str(e)}")
        raise e


if __name__ == "__main__":
    run_data_cleaning_pipeline()
