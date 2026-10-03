import os
import logging
from flask_pymongo import PyMongo
from pymongo import MongoClient

logger = logging.getLogger(__name__)

mongo = PyMongo()
_fallback_client = None

def init_db(app):
    """
    Initialize database connection with resilient fallback handling.
    """
    try:
        mongo.init_app(app)
        # Test connection
        mongo.db.command('ping')
        app.logger.info("Connected to MongoDB via Flask-PyMongo successfully.")
    except Exception as e:
        app.logger.warning(f"Flask-PyMongo direct ping failed ({e}). Attempting PyMongo direct fallback...")
        try:
            uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/aptiforge')
            global _fallback_client
            _fallback_client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            _fallback_client.admin.command('ping')
            app.logger.info("Connected to MongoDB via direct PyMongo fallback.")
        except Exception as err:
            app.logger.error(f"MongoDB connection failed: {err}. Please make sure MongoDB is running or MONGO_URI is set.")

def get_db():
    try:
        if mongo.db is not None:
            return mongo.db
    except Exception:
        pass
    if _fallback_client:
        db_name = _fallback_client.get_default_database().name if _fallback_client.get_default_database() else 'aptiforge'
        return _fallback_client[db_name]
    return mongo.db
