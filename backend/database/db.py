"""
Database initialization
Sets up MongoDB connection using MongoEngine
"""

from flask_mongoengine import MongoEngine

db = MongoEngine()

def init_db(app):
    """Initialize database connection"""
    db.init_app(app)
    return db

