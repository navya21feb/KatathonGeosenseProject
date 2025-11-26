"""
Helper utility functions
Common helper functions used across the application
"""

from datetime import datetime, timedelta
import json

def format_coordinates(lat, lon):
    """Format coordinates for API responses"""
    return {
        'latitude': float(lat),
        'longitude': float(lon)
    }

def calculate_distance(point1, point2):
    """Calculate distance between two points"""
    from geopy.distance import distance
    return distance(point1, point2).kilometers

def format_datetime(dt):
    """Format datetime for API responses"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.isoformat()

def parse_time_range(time_range):
    """Parse time range string (e.g., '6-8 PM')"""
    # TODO: Implement time range parsing
    pass

