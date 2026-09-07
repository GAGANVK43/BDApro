"""
analytics_routes.py - Flask REST API Endpoints
Provides JSON responses for dashboard charts, KPIs, movie explorer, database status, and pipeline control.
"""

from flask import Blueprint, jsonify, request
from services.analytics_service import (
    parse_filters,
    fetch_summary,
    fetch_genres,
    fetch_ratings,
    fetch_releases,
    fetch_countries,
    fetch_top_movies,
    fetch_movies_paginated,
    fetch_movie_detail,
    fetch_filter_metadata
)
from services.mongodb_service import get_database_health
from services.pipeline_service import get_pipeline_health, trigger_data_cleaning, trigger_mongodb_sync

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/summary", methods=["GET"])
def api_summary():
    """Returns top KPI statistics and dynamically generated natural language insights."""
    filters = parse_filters(request.args)
    data = fetch_summary(filters)
    return jsonify({"status": "success", "data": data})


@api_bp.route("/genres", methods=["GET"])
def api_genres():
    """Returns genre distribution and metrics."""
    filters = parse_filters(request.args)
    top_n = request.args.get("top_n", 15, type=int)
    data = fetch_genres(filters, top_n=top_n)
    return jsonify({"status": "success", "data": data})


@api_bp.route("/ratings", methods=["GET"])
def api_ratings():
    """Returns content maturity rating breakdown."""
    filters = parse_filters(request.args)
    data = fetch_ratings(filters)
    return jsonify({"status": "success", "data": data})


@api_bp.route("/releases", methods=["GET"])
def api_releases():
    """Returns annual release trends and cumulative growth."""
    filters = parse_filters(request.args)
    data = fetch_releases(filters)
    return jsonify({"status": "success", "data": data})


@api_bp.route("/countries", methods=["GET"])
def api_countries():
    """Returns country production distribution."""
    filters = parse_filters(request.args)
    top_n = request.args.get("top_n", 12, type=int)
    data = fetch_countries(filters, top_n=top_n)
    return jsonify({"status": "success", "data": data})


@api_bp.route("/top-movies", methods=["GET"])
def api_top_movies():
    """Returns highest-rated movies/shows."""
    filters = parse_filters(request.args)
    limit = request.args.get("limit", 10, type=int)
    data = fetch_top_movies(filters, limit=limit)
    return jsonify({"status": "success", "data": data})


@api_bp.route("/movies", methods=["GET"])
def api_movies():
    """Returns paginated movie explorer list."""
    filters = parse_filters(request.args)
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 12, type=int)
    data = fetch_movies_paginated(filters, page=page, page_size=page_size)
    return jsonify({"status": "success", "data": data})


@api_bp.route("/movie/<show_id>", methods=["GET"])
def api_movie_detail(show_id):
    """Returns full metadata for a single show/movie."""
    data = fetch_movie_detail(show_id)
    if data["found"]:
        return jsonify({"status": "success", "data": data["movie"]})
    return jsonify({"status": "error", "message": "Movie not found"}), 404


@api_bp.route("/filters", methods=["GET"])
def api_filters():
    """Returns available unique filter options (genres, countries, ratings, years)."""
    data = fetch_filter_metadata()
    return jsonify({"status": "success", "data": data})


@api_bp.route("/pipeline-status", methods=["GET"])
def api_pipeline_status():
    """Returns live infrastructure status across Hadoop, Hive, MongoDB, Python, Datasets."""
    health = get_pipeline_health()
    return jsonify({"status": "success", "data": health})


@api_bp.route("/database-status", methods=["GET"])
def api_database_status():
    """Returns live MongoDB Atlas status, collections, and document counts."""
    db_health = get_database_health()
    return jsonify({"status": "success", "data": db_health})


@api_bp.route("/pipeline/clean", methods=["POST"])
def api_trigger_clean():
    """Triggers the Python data cleaning pipeline."""
    res = trigger_data_cleaning()
    return jsonify(res)


@api_bp.route("/pipeline/sync-mongodb", methods=["POST"])
def api_trigger_mongodb_sync():
    """Triggers cleaned data ingestion into MongoDB Atlas."""
    res = trigger_mongodb_sync()
    return jsonify(res)
