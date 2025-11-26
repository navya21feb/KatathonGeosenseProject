"""
Insights API endpoints
Handles traffic insights, POI analysis, and mobility patterns
"""

from flask import Blueprint, jsonify, request
from services.traffic_api import TrafficAPI
from services.data_processor import DataProcessor
import logging

logger = logging.getLogger(__name__)
insights_bp = Blueprint('insights', __name__)
traffic_api = TrafficAPI()

@insights_bp.route('/traffic', methods=['GET'])
def get_traffic_insights():
    """
    Get traffic insights for a given location
    
    Query parameters:
    - lat: latitude
    - lon: longitude
    - zoom: zoom level (optional, default 10)
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        zoom = request.args.get('zoom', default=10, type=int)
        
        if lat is None or lon is None:
            return jsonify({
                'success': False,
                'error': 'Missing required parameters: lat, lon'
            }), 400
        
        # Get traffic flow data
        flow_data = traffic_api.get_traffic_flow(lat, lon, zoom)
        
        if not flow_data.get('success'):
            return jsonify(flow_data), 500
        
        # Get nearby incidents
        bbox = f"{lon-0.1},{lat-0.1},{lon+0.1},{lat+0.1}"
        incidents = traffic_api.get_traffic_incidents(bbox)
        
        return jsonify({
            'success': True,
            'location': {'lat': lat, 'lon': lon},
            'traffic_flow': flow_data,
            'incidents': incidents
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_traffic_insights: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@insights_bp.route('/busiest-hours', methods=['GET'])
def get_busiest_hours():
    """
    Get busiest hours analysis for a location
    Analyzes traffic patterns throughout the day
    
    Query parameters:
    - lat: latitude
    - lon: longitude
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if lat is None or lon is None:
            return jsonify({
                'success': False,
                'error': 'Missing required parameters: lat, lon'
            }), 400
        
        # Get current traffic data
        current_traffic = traffic_api.get_traffic_flow(lat, lon)
        
        if not current_traffic.get('success'):
            return jsonify(current_traffic), 500
        
        # Generate typical hourly patterns (this would ideally use historical data)
        busiest_hours = DataProcessor.analyze_busiest_hours(lat, lon, current_traffic)
        
        return jsonify({
            'success': True,
            'location': {'lat': lat, 'lon': lon},
            'busiest_hours': busiest_hours,
            'current_hour_status': {
                'congestion_level': current_traffic.get('congestion_level'),
                'current_speed': current_traffic.get('current_speed'),
                'free_flow_speed': current_traffic.get('free_flow_speed')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_busiest_hours: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@insights_bp.route('/poi-analysis', methods=['GET'])
def get_poi_analysis():
    """
    Analyze Points of Interest in an area
    
    Query parameters:
    - lat: latitude
    - lon: longitude
    - radius: search radius in meters (optional, default 5000)
    - category: POI category filter (optional)
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        radius = request.args.get('radius', default=5000, type=int)
        category = request.args.get('category', default=None, type=str)
        
        if lat is None or lon is None:
            return jsonify({
                'success': False,
                'error': 'Missing required parameters: lat, lon'
            }), 400
        
        # Search for POIs
        pois = traffic_api.search_nearby_pois(lat, lon, radius, category)
        
        if not pois.get('success'):
            return jsonify(pois), 500
        
        # Analyze POI distribution
        analysis = DataProcessor.analyze_poi_distribution(pois.get('pois', []))
        
        return jsonify({
            'success': True,
            'location': {'lat': lat, 'lon': lon},
            'search_radius_meters': radius,
            'pois': pois.get('pois', []),
            'analysis': analysis
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_poi_analysis: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@insights_bp.route('/mobility-patterns', methods=['GET'])
def get_mobility_patterns():
    """
    Get mobility patterns for an area
    Combines traffic, POI, and incident data for comprehensive insights
    
    Query parameters:
    - lat: latitude
    - lon: longitude
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if lat is None or lon is None:
            return jsonify({
                'success': False,
                'error': 'Missing required parameters: lat, lon'
            }), 400
        
        # Get traffic data
        traffic_flow = traffic_api.get_traffic_flow(lat, lon)
        
        # Get incidents
        bbox = f"{lon-0.1},{lat-0.1},{lon+0.1},{lat+0.1}"
        incidents = traffic_api.get_traffic_incidents(bbox)
        
        # Get POIs
        pois = traffic_api.search_nearby_pois(lat, lon, 5000)
        
        # Generate mobility insights
        patterns = DataProcessor.generate_mobility_patterns(
            traffic_flow, 
            incidents.get('incidents', []),
            pois.get('pois', [])
        )
        
        return jsonify({
            'success': True,
            'location': {'lat': lat, 'lon': lon},
            'patterns': patterns,
            'summary': {
                'congestion_level': traffic_flow.get('congestion_level', 'unknown'),
                'active_incidents': incidents.get('incident_count', 0),
                'nearby_pois': pois.get('poi_count', 0)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_mobility_patterns: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@insights_bp.route('/area-classification', methods=['GET'])
def get_area_classification():
    """
    Classify an area based on its characteristics
    Examples: "Commercial hub", "Residential quiet zone", "Entertainment district"
    
    Query parameters:
    - lat: latitude
    - lon: longitude
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if lat is None or lon is None:
            return jsonify({
                'success': False,
                'error': 'Missing required parameters: lat, lon'
            }), 400
        
        # Get POIs for classification
        pois = traffic_api.search_nearby_pois(lat, lon, 2000)
        
        # Get traffic data
        traffic_flow = traffic_api.get_traffic_flow(lat, lon)
        
        # Classify the area
        classification = DataProcessor.classify_area(
            pois.get('pois', []),
            traffic_flow
        )
        
        return jsonify({
            'success': True,
            'location': {'lat': lat, 'lon': lon},
            'classification': classification
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_area_classification: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@insights_bp.route('/test', methods=['GET'])
def test_insights():
    """Test endpoint to verify insights service is working"""
    return jsonify({
        'success': True,
        'message': 'Insights service is operational',
        'available_endpoints': [
            'GET /api/insights/traffic?lat=X&lon=Y',
            'GET /api/insights/busiest-hours?lat=X&lon=Y',
            'GET /api/insights/poi-analysis?lat=X&lon=Y&radius=5000',
            'GET /api/insights/mobility-patterns?lat=X&lon=Y',
            'GET /api/insights/area-classification?lat=X&lon=Y'
        ]
    }), 200