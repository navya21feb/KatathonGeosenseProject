"""
Configuration settings for GeoSense backend
Loads environment variables and sets up app configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/geosense')
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'geosense')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # API Keys
    TOMTOM_API_KEY = os.getenv('TOMTOM_API_KEY', '')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # Report Generation
    REPORT_OUTPUT_DIR = os.getenv('REPORT_OUTPUT_DIR', 'reports')

