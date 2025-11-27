"""
Helper utility functions
Common helper functions used across the application
"""

from datetime import datetime, timedelta
from geopy.distance import distance as geopy_distance
import json
import re

def format_coordinates(lat, lon):
    """
    Format coordinates for API responses
    """
    return {
        'latitude': float(lat),
        'longitude': float(lon)
    }

def calculate_distance(point1, point2):
    """
    Calculate distance between two points in kilometers
    
    point1: tuple (lat, lon) or dict with 'lat' and 'lon'
    point2: tuple (lat, lon) or dict with 'lat' and 'lon'
    
    Returns: distance in kilometers
    """
    # Convert to tuple if dict
    if isinstance(point1, dict):
        point1 = (point1['lat'], point1['lon'])
    if isinstance(point2, dict):
        point2 = (point2['lat'], point2['lon'])
    
    return geopy_distance(point1, point2).kilometers

def format_datetime(dt):
    """
    Format datetime for API responses
    """
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except:
            return dt
    
    if isinstance(dt, datetime):
        return dt.isoformat()
    
    return str(dt)

def parse_time_range(time_range):
    """
    Parse time range string (e.g., '6-8 PM', '07:00-09:00')
    
    Returns: dict with 'start_hour' and 'end_hour'
    """
    try:
        # Handle formats like "6-8 PM" or "6-8 AM"
        pattern1 = r'(\d+)-(\d+)\s*(AM|PM|am|pm)'
        match1 = re.match(pattern1, time_range.strip())
        
        if match1:
            start = int(match1.group(1))
            end = int(match1.group(2))
            period = match1.group(3).upper()
            
            if period == 'PM' and start < 12:
                start += 12
            if period == 'PM' and end < 12:
                end += 12
            
            return {
                'start_hour': start,
                'end_hour': end,
                'formatted': f"{start:02d}:00 - {end:02d}:00"
            }
        
        # Handle formats like "07:00-09:00"
        pattern2 = r'(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})'
        match2 = re.match(pattern2, time_range.strip())
        
        if match2:
            start = int(match2.group(1))
            end = int(match2.group(3))
            
            return {
                'start_hour': start,
                'end_hour': end,
                'formatted': f"{start:02d}:{match2.group(2)} - {end:02d}:{match2.group(4)}"
            }
        
        return None
        
    except Exception as e:
        return None

def calculate_bbox(lat, lon, radius_km):
    """
    Calculate bounding box around a point
    
    lat, lon: center point coordinates
    radius_km: radius in kilometers
    
    Returns: bbox string "minLon,minLat,maxLon,maxLat"
    """
    # Approximate degrees per km (rough estimate)
    lat_degree = radius_km / 111.0
    lon_degree = radius_km / (111.0 * abs(geopy_distance.cosine(lat)))
    
    min_lat = lat - lat_degree
    max_lat = lat + lat_degree
    min_lon = lon - lon_degree
    max_lon = lon + lon_degree
    
    return f"{min_lon},{min_lat},{max_lon},{max_lat}"

def format_duration(seconds):
    """
    Format duration in seconds to human-readable format
    
    Returns: string like "2h 30m" or "45m"
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    
    minutes = seconds / 60
    
    if minutes < 60:
        return f"{int(minutes)}m"
    
    hours = int(minutes / 60)
    remaining_minutes = int(minutes % 60)
    
    if remaining_minutes == 0:
        return f"{hours}h"
    
    return f"{hours}h {remaining_minutes}m"

def format_distance(meters):
    """
    Format distance in meters to human-readable format
    
    Returns: string like "5.2 km" or "850 m"
    """
    if meters < 1000:
        return f"{int(meters)} m"
    
    km = meters / 1000
    return f"{km:.1f} km"

def categorize_congestion(speed_ratio):
    """
    Categorize congestion level based on speed ratio
    
    speed_ratio: current_speed / free_flow_speed
    
    Returns: congestion level string
    """
    if speed_ratio >= 0.8:
        return 'low'
    elif speed_ratio >= 0.5:
        return 'moderate'
    elif speed_ratio >= 0.3:
        return 'high'
    else:
        return 'severe'

def get_time_period():
    """
    Get current time period (morning, afternoon, evening, night)
    """
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'

def is_peak_hour(hour=None):
    """
    Check if given hour is a peak traffic hour
    
    hour: hour of day (0-23), defaults to current hour
    """
    if hour is None:
        hour = datetime.now().hour
    
    # Peak hours: 7-9 AM and 5-7 PM on weekdays
    day_of_week = datetime.now().weekday()
    
    if day_of_week < 5:  # Weekday
        return (7 <= hour <= 9) or (17 <= hour <= 19)
    
    return False

def calculate_estimated_cost(distance_km, cost_per_km=0.15):
    """
    Calculate estimated travel cost based on distance
    
    distance_km: distance in kilometers
    cost_per_km: cost per kilometer (default $0.15)
    
    Returns: estimated cost in USD
    """
    return round(distance_km * cost_per_km, 2)

def calculate_co2_emission(distance_km, emission_factor=0.12):
    """
    Calculate CO2 emission based on distance
    
    distance_km: distance in kilometers
    emission_factor: kg CO2 per km (default 0.12 for average car)
    
    Returns: CO2 emission in kg
    """
    return round(distance_km * emission_factor, 2)

def parse_coordinates_string(coord_string):
    """
    Parse coordinate string to lat/lon dict
    
    Supports formats:
    - "28.6139,77.2090"
    - "28.6139, 77.2090"
    - "[28.6139, 77.2090]"
    
    Returns: dict with 'lat' and 'lon'
    """
    try:
        # Remove brackets and split
        coord_string = coord_string.strip('[]')
        parts = [p.strip() for p in coord_string.split(',')]
        
        if len(parts) == 2:
            return {
                'lat': float(parts[0]),
                'lon': float(parts[1])
            }
        
        return None
        
    except Exception as e:
        return None

def format_api_response(success, data=None, error=None, message=None):
    """
    Format standardized API response
    """
    response = {
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    
    if error is not None:
        response['error'] = error
    
    if message is not None:
        response['message'] = message
    
    return response

def merge_route_segments(segments):
    """
    Merge multiple route segments into a single route
    
    segments: list of route coordinate arrays
    
    Returns: merged coordinate array
    """
    merged = []
    
    for segment in segments:
        if segment:
            if merged and len(merged) > 0 and len(segment) > 0:
                # Skip first point of new segment if it duplicates last point
                if merged[-1] == segment[0]:
                    merged.extend(segment[1:])
                else:
                    merged.extend(segment)
            else:
                merged.extend(segment)
    
    return merged

def simplify_coordinates(coords, tolerance=0.0001):
    """
    Simplify coordinate array by removing points within tolerance
    Useful for reducing payload size
    
    coords: list of [lat, lon] coordinates
    tolerance: minimum difference to keep a point
    
    Returns: simplified coordinate list
    """
    if len(coords) <= 2:
        return coords
    
    simplified = [coords[0]]
    
    for i in range(1, len(coords) - 1):
        prev = simplified[-1]
        curr = coords[i]
        
        if abs(curr[0] - prev[0]) > tolerance or abs(curr[1] - prev[1]) > tolerance:
            simplified.append(curr)
    
    simplified.append(coords[-1])
    
    return simplified

def validate_geojson(geojson_data):
    """
    Validate GeoJSON format
    
    Returns: (is_valid, error_message)
    """
    try:
        if not isinstance(geojson_data, dict):
            return False, "GeoJSON must be an object"
        
        if 'type' not in geojson_data:
            return False, "Missing 'type' field"
        
        valid_types = ['Point', 'LineString', 'Polygon', 'Feature', 'FeatureCollection']
        if geojson_data['type'] not in valid_types:
            return False, f"Invalid type. Must be one of {valid_types}"
        
        return True, None
        
    except Exception as e:
        return False, str(e)
    
def validate_coordinates(lat, lon):
    """Validate latitude and longitude values."""
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return False, "Latitude and longitude must be numeric."

    if not (-90 <= lat <= 90):
        return False, "Latitude must be between -90 and 90."
    if not (-180 <= lon <= 180):
        return False, "Longitude must be between -180 and 180."

    return True, None
