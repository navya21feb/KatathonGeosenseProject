"""
Input validation utilities
Validates API request parameters
"""

def validate_coordinates(lat, lon):
    """Validate latitude and longitude"""
    try:
        lat = float(lat)
        lon = float(lon)
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return lat, lon
    except (ValueError, TypeError):
        raise ValueError("Invalid coordinates")

def validate_route_params(data):
    """Validate route calculation parameters"""
    required = ['origin', 'destination']
    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    validate_coordinates(data['origin']['lat'], data['origin']['lon'])
    validate_coordinates(data['destination']['lat'], data['destination']['lon'])
    
    return True

def validate_report_params(data):
    """Validate report generation parameters"""
    required = ['report_type', 'stakeholder_type']
    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    valid_stakeholders = ['government', 'researcher', 'engineer']
    if data['stakeholder_type'] not in valid_stakeholders:
        raise ValueError(f"Invalid stakeholder type. Must be one of: {valid_stakeholders}")
    
    return True

