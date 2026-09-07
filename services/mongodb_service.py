"""
mongodb_service.py - Production MongoDB Atlas Service Layer
Provides connection pooling, querying, aggregation pipelines, and collections inspection.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Load environment variables
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

DEFAULT_DB_NAME = os.getenv("MONGODB_DB_NAME", "netflix_analytics")

# Reusable MongoClient instance
_mongo_client = None


def get_client(timeout_ms: int = 3000):
    """Returns a singleton PyMongo client with timeout handling."""
    global _mongo_client
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        return None

    if _mongo_client is None:
        try:
            _mongo_client = pymongo.MongoClient(
                uri,
                serverSelectionTimeoutMS=timeout_ms,
                connectTimeoutMS=timeout_ms,
                appname="NetflixFlaskAnalytics"
            )
            # Test ping
            _mongo_client.admin.command('ping')
        except Exception:
            _mongo_client = None
            return None
            
    return _mongo_client


def get_db():
    """Returns MongoDB database instance or None."""
    client = get_client()
    if client is not None:
        db_name = os.getenv("MONGODB_DB_NAME", DEFAULT_DB_NAME)
        return client[db_name]
    return None


def get_database_health() -> dict:
    """Returns detailed database health, collections, and document counts."""
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        return {
            "connected": False,
            "status": "NOT CONFIGURED",
            "db_name": DEFAULT_DB_NAME,
            "message": "MONGODB_URI is not configured in environment variables.",
            "collections": {},
            "total_documents": 0
        }

    try:
        # Create a fresh client check if singleton is disconnected
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=2500, connectTimeoutMS=2500)
        client.admin.command('ping')
        db_name = os.getenv("MONGODB_DB_NAME", DEFAULT_DB_NAME)
        db = client[db_name]
        
        collection_names = db.list_collection_names()
        counts = {}
        total_docs = 0
        for col_name in collection_names:
            cnt = db[col_name].count_documents({})
            counts[col_name] = cnt
            total_docs += cnt
            
        # Mask credentials in URI for safe display
        masked_uri = uri
        if "@" in uri:
            prefix = uri.split("@")[0].split("://")[0] + "://***:***@"
            suffix = uri.split("@")[1]
            masked_uri = prefix + suffix

        return {
            "connected": True,
            "status": "CONNECTED",
            "db_name": db_name,
            "uri": masked_uri,
            "message": f"Connected successfully to MongoDB Atlas ({len(collection_names)} collections found).",
            "collections": counts,
            "total_documents": total_docs
        }
    except Exception as e:
        return {
            "connected": False,
            "status": "DISCONNECTED",
            "db_name": DEFAULT_DB_NAME,
            "message": f"MongoDB connection error: {str(e)}",
            "collections": {},
            "total_documents": 0
        }


def query_collection(collection_name: str, query: dict = None, projection: dict = None, sort=None, limit: int = 0):
    """Queries a MongoDB collection if available."""
    db = get_db()
    if db is None:
        return None
    try:
        col = db[collection_name]
        cursor = col.find(query or {}, projection or {"_id": 0})
        if sort:
            cursor = cursor.sort(sort)
        if limit > 0:
            cursor = cursor.limit(limit)
        return list(cursor)
    except Exception:
        return None


def run_aggregation(collection_name: str, pipeline: list):
    """Executes a MongoDB aggregation pipeline."""
    db = get_db()
    if db is None:
        return None
    try:
        col = db[collection_name]
        return list(col.aggregate(pipeline))
    except Exception:
        return None
