"""
Database Helper Functions

MongoDB helper functions ready to use in your backend code.
Import and use these functions in your API endpoints for database operations.
"""

from pymongo import MongoClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from typing import Union
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

_client = None
db = None

database_url = os.getenv("DATABASE_URL")
database_name = os.getenv("DATABASE_NAME")

# Initialize client safely so the API can still start even if DB isn't available
if database_url and database_name:
    try:
        _client = MongoClient(database_url)
        db = _client[database_name]
    except Exception as e:
        # Failed to initialize database (e.g., missing dnspython for mongodb+srv, DNS issues, etc.)
        # Defer raising until an operation is attempted so the server can start.
        db = None
        os.environ["DB_INIT_ERROR"] = str(e)

# Helper functions for common database operations

def create_document(collection_name: str, data: Union[BaseModel, dict]):
    """Insert a single document with timestamp"""
    if db is None:
        init_error = os.getenv("DB_INIT_ERROR")
        raise Exception(
            "Database not available. Check DATABASE_URL and DATABASE_NAME environment variables."
            + (f" Init error: {init_error}" if init_error else "")
        )

    # Convert Pydantic model to dict if needed
    if isinstance(data, BaseModel):
        data_dict = data.model_dump()
    else:
        data_dict = data.copy()

    data_dict['created_at'] = datetime.now(timezone.utc)
    data_dict['updated_at'] = datetime.now(timezone.utc)

    result = db[collection_name].insert_one(data_dict)
    return str(result.inserted_id)


def get_documents(collection_name: str, filter_dict: dict = None, limit: int = None):
    """Get documents from collection"""
    if db is None:
        init_error = os.getenv("DB_INIT_ERROR")
        raise Exception(
            "Database not available. Check DATABASE_URL and DATABASE_NAME environment variables."
            + (f" Init error: {init_error}" if init_error else "")
        )
    
    cursor = db[collection_name].find(filter_dict or {})
    if limit:
        cursor = cursor.limit(limit)
    
    return list(cursor)
