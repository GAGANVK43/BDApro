"""
analytics_service.py - Hybrid Big Data Analytics Service
Executes MongoDB aggregations when connected, or falls back to cleaned DataFrame analytics.
Generates dynamic natural language insights and formatted JSON API outputs.
"""

from pathlib import Path
import pandas as pd
import numpy as np

from python.analytics import (
    load_cleaned_dataframe,
    filter_dataframe,
    get_dashboard_summary,
    get_genre_statistics,
    get_release_statistics,
    get_rating_statistics,
    get_country_statistics,
    get_top_rated_movies,
    get_dynamic_insights
)
from services.mongodb_service import get_db, run_aggregation, query_collection


def parse_filters(args: dict) -> dict:
    """Parses query string arguments from Flask request into standardized filters."""
    filters = {}
    
    # Year Range
    min_year = args.get("min_year")
    max_year = args.get("max_year")
    if min_year and max_year:
        try:
            filters["year_range"] = (int(min_year), int(max_year))
        except ValueError:
            pass
            
    # Content Types
    types = args.get("types")
    if types:
        types_list = [t.strip() for t in types.split(",") if t.strip()]
        if types_list and "All" not in types_list:
            filters["content_types"] = types_list
            
    # Genres
    genres = args.get("genres")
    if genres:
        genre_list = [g.strip() for g in genres.split(",") if g.strip()]
        if genre_list and "All" not in genre_list:
            filters["genres"] = genre_list
            
    # Countries
    countries = args.get("countries")
    if countries:
        c_list = [c.strip() for c in countries.split(",") if c.strip()]
        if c_list and "All" not in c_list:
            filters["countries"] = c_list
            
    # Ratings
    ratings = args.get("ratings")
    if ratings:
        r_list = [r.strip() for r in ratings.split(",") if r.strip()]
        if r_list and "All" not in r_list:
            filters["ratings"] = r_list
            
    # Search Query
    q = args.get("q")
    if q and q.strip():
        filters["search_query"] = q.strip()
        
    return filters


def get_filtered_df(filters: dict = None) -> pd.DataFrame:
    """Returns filtered Pandas DataFrame from cleaned data source."""
    df = load_cleaned_dataframe()
    if not filters:
        return df
        
    return filter_dataframe(
        df,
        year_range=filters.get("year_range"),
        content_types=filters.get("content_types"),
        genres=filters.get("genres"),
        countries=filters.get("countries"),
        ratings=filters.get("ratings"),
        search_query=filters.get("search_query")
    )


def fetch_summary(filters: dict = None) -> dict:
    """Returns top KPI cards and dynamic insights."""
    df = get_filtered_df(filters)
    summary = get_dashboard_summary(df)
    insights = get_dynamic_insights(df)
    
    return {
        "kpis": summary,
        "insights": insights,
        "total_records_analyzed": len(df)
    }


def fetch_genres(filters: dict = None, top_n: int = 15) -> list[dict]:
    """Returns genre distribution and metrics."""
    df = get_filtered_df(filters)
    genre_df = get_genre_statistics(df, top_n=top_n)
    if genre_df.empty:
        return []
    return genre_df.to_dict(orient="records")


def fetch_ratings(filters: dict = None) -> list[dict]:
    """Returns rating distribution."""
    df = get_filtered_df(filters)
    r_df = get_rating_statistics(df)
    if r_df.empty:
        return []
    return r_df.to_dict(orient="records")


def fetch_releases(filters: dict = None) -> list[dict]:
    """Returns release year timeline statistics."""
    df = get_filtered_df(filters)
    rel_df = get_release_statistics(df)
    if rel_df.empty:
        return []
    return rel_df.to_dict(orient="records")


def fetch_countries(filters: dict = None, top_n: int = 12) -> list[dict]:
    """Returns country distribution."""
    df = get_filtered_df(filters)
    c_df = get_country_statistics(df, top_n=top_n)
    if c_df.empty:
        return []
    return c_df.to_dict(orient="records")


def fetch_top_movies(filters: dict = None, limit: int = 10) -> list[dict]:
    """Returns top-rated movie titles."""
    df = get_filtered_df(filters)
    top_df = get_top_rated_movies(df, limit=limit)
    if top_df.empty:
        return []
    return top_df.to_dict(orient="records")


def fetch_movies_paginated(filters: dict = None, page: int = 1, page_size: int = 12) -> dict:
    """Returns paginated movie explorer list with total count."""
    df = get_filtered_df(filters)
    total_count = len(df)
    
    # Calculate slice
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    page_df = df.iloc[start_idx:end_idx]
    
    # Fill NaN with empty string
    page_df = page_df.fillna("")
    movies = page_df.to_dict(orient="records")
    
    total_pages = max(1, (total_count + page_size - 1) // page_size)
    
    return {
        "movies": movies,
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages
    }


def fetch_movie_detail(show_id: str) -> dict:
    """Returns full metadata for a single title."""
    df = load_cleaned_dataframe()
    matched = df[df["show_id"].astype(str) == str(show_id)]
    if matched.empty:
        # Fallback search by title
        matched = df[df["title"].astype(str).str.lower() == str(show_id).lower()]
        
    if not matched.empty:
        row = matched.iloc[0].fillna("").to_dict()
        return {"found": True, "movie": row}
        
    return {"found": False, "movie": None}


def fetch_filter_metadata() -> dict:
    """Extracts all unique filter options from the dataset."""
    df = load_cleaned_dataframe()
    if df.empty:
        return {"min_year": 1990, "max_year": 2024, "genres": [], "countries": [], "ratings": [], "types": []}
        
    # Unique Genres
    all_genres = set()
    for g_str in df["listed_in"].dropna():
        for g in str(g_str).split(","):
            if g.strip():
                all_genres.add(g.strip())
                
    # Unique Countries
    all_countries = set()
    for c_str in df["country"].dropna():
        for c in str(c_str).split(","):
            c_clean = c.strip()
            if c_clean and c_clean != "Unknown":
                all_countries.add(c_clean)
                
    return {
        "min_year": int(df["release_year"].min()),
        "max_year": int(df["release_year"].max()),
        "genres": sorted(list(all_genres)),
        "countries": sorted(list(all_countries)),
        "ratings": sorted(list(df["rating"].dropna().unique())),
        "types": sorted(list(df["type"].dropna().unique()))
    }
