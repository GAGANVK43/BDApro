"""
mongodb_connection.py - MongoDB Atlas / Local Connection Handler
Handles secure connection via MONGODB_URI environment variable with timeout and status reporting.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError

# Load environment variables
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

DEFAULT_DB_NAME = os.getenv("MONGODB_DB_NAME", "netflix_analytics")


def get_mongodb_uri() -> str:
    """Retrieves MongoDB URI from environment variable or default local."""
    return os.getenv("MONGODB_URI", "").strip()


def connect_mongodb(timeout_ms: int = 3000):
    """
    Connects to MongoDB using MONGODB_URI.
    Returns:
        (db, client, None) if successful
        (None, None, error_message) if connection fails
    """
    uri = get_mongodb_uri()
    if not uri:
        return None, None, "MONGODB_URI is not set in environment or .env file."

    try:
        # Create client with safe connection timeout
        client = pymongo.MongoClient(
            uri,
            serverSelectionTimeoutMS=timeout_ms,
            connectTimeoutMS=timeout_ms,
            appname="NetflixAnalyticsPlatform"
        )
        # Test connection with ping command
        client.admin.command('ping')
        db_name = os.getenv("MONGODB_DB_NAME", DEFAULT_DB_NAME)
        db = client[db_name]
        return db, client, None
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        return None, None, f"Could not connect to MongoDB server: {str(e)}"
    except ConfigurationError as e:
        return None, None, f"MongoDB URI configuration error: {str(e)}"
    except Exception as e:
        return None, None, f"Unexpected MongoDB error: {str(e)}"


def check_mongodb_status() -> dict:
    """
    Performs a live health check on the MongoDB connection.
    Returns status dictionary.
    """
    uri = get_mongodb_uri()
    if not uri:
        return {
            "connected": False,
            "status": "NOT CONFIGURED",
            "db_name": DEFAULT_DB_NAME,
            "details": "MONGODB_URI environment variable is missing. Set it in config/.env to connect."
        }

    db, client, error = connect_mongodb(timeout_ms=2500)
    if error or db is None:
        # Mask credentials in URI for safe display
        masked_uri = uri
        if "@" in uri:
            prefix = uri.split("@")[0].split("://")[0] + "://***:***@"
            suffix = uri.split("@")[1]
            masked_uri = prefix + suffix

        return {
            "connected": False,
            "status": "NOT CONNECTED",
            "db_name": DEFAULT_DB_NAME,
            "uri": masked_uri,
            "details": f"Connection failed: {error}"
        }

    try:
        collections = db.list_collection_names()
        doc_count = db["movies"].count_documents({}) if "movies" in collections else 0
        client.close()
        return {
            "connected": True,
            "status": "CONNECTED / READY",
            "db_name": db.name,
            "collections": collections,
            "movies_count": doc_count,
            "details": f"Successfully connected to MongoDB Atlas / Local ({len(collections)} collections found)."
        }
    except Exception as e:
        return {
            "connected": False,
            "status": "CONNECTED (LIMITED)",
            "details": f"Connected but failed to list collections: {str(e)}"
        }
