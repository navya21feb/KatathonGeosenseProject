"""
Insights API endpoints - FIXED VERSION
Handles traffic insights, POI analysis, and mobility patterns
"""

from flask import Blueprint, jsonify, request
from services.traffic_api import TrafficAPI
from services.data_processor import DataProcessor
from utils.helpers import format_api_response, validate_coordinates
import logging

logger = logging.getLogger(__name__)
insights_bp = Blueprint('insights', __name__)
traffic_api = TrafficAPI()
data_processor = DataProcessor()

@insights_bp.route('/traffic', methods=['GET'])
def get_traffic_insights():
    """
    Get traffic insights for a given location
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        zoom = request.args.get('zoom', default=10, type=int)
        
        # Validate coordinates
        valid, error = validate_coordinates(lat, lon)
        if not valid:
            return jsonify(format_api_response(False, error=error)), 400
        
        # Get traffic flow data
        flow_data = traffic_api.get_traffic_flow(lat, lon)
        
        if not flow_data:
            return jsonify(format_api_response(False, error="Failed to fetch traffic data")), 500
        
        # Get nearby incidents
        from utils.helpers import calculate_bbox
        bbox = calculate_bbox(lat, lon, 5)  # 5km radius
        incidents = traffic_api.get_traffic_incidents(bbox)
        
        return jsonify(format_api_response(True, data={
            'location': {'lat': lat, 'lon': lon},
            'traffic_flow': flow_data,
            'incidents': incidents,
            'zoom_level': zoom
        })), 200
        
    except Exception as e:
        logger.error(f"Error in get_traffic_insights: {e}")
        return jsonify(format_api_response(False, error=str(e))), 500

@insights_bp.route('/busiest-hours', methods=['GET'])
def get_busiest_hours():
    """
    Get busiest hours analysis for a location
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        days = request.args.get('days', default=7, type=int)
        
        # Validate coordinates
        valid, error = validate_coordinates(lat, lon)
        if not valid:
            return jsonify(format_api_response(False, error=error)), 400
        
        # Get busiest hours analysis
        analysis = traffic_api.get_busiest_hours_analysis(lat, lon, days)
        
        return jsonify(format_api_response(True, data={
            'location': {'lat': lat, 'lon': lon},
            'analysis_period_days': days,
            'analysis': analysis
        })), 200
        
    except Exception as e:
        logger.error(f"Error in get_busiest_hours: {e}")
        return jsonify(format_api_response(False, error=str(e))), 500

@insights_bp.route('/poi-analysis', methods=['GET'])
def get_poi_analysis():
    """
    Analyze Points of Interest in an area
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        radius = request.args.get('radius', default=5000, type=int)
        category = request.args.get('category', default=None, type=str)
        
        # Validate coordinates
        valid, error = validate_coordinates(lat, lon)
        if not valid:
            return jsonify(format_api_response(False, error=error)), 400
        
        # Search for POIs
        pois = traffic_api.search_poi(lat, lon, radius, category)
        
        # Analyze POI distribution
        analysis = data_processor.analyze_poi_distribution(pois)
        
        return jsonify(format_api_response(True, data={
            'location': {'lat': lat, 'lon': lon},
            'search_radius_meters': radius,
            'pois_found': len(pois),
            'pois': pois,
            'analysis': analysis
        })), 200
        
    except Exception as e:
        logger.error(f"Error in get_poi_analysis: {e}")
        return jsonify(format_api_response(False, error=str(e))), 500

@insights_bp.route('/mobility-patterns', methods=['GET'])
def get_mobility_patterns():
    """
    Get comprehensive mobility patterns for an area
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        # Validate coordinates
        valid, error = validate_coordinates(lat, lon)
        if not valid:
            return jsonify(format_api_response(False, error=error)), 400
        
        # Get all data for mobility analysis
        traffic_flow = traffic_api.get_traffic_flow(lat, lon)
        bbox = calculate_bbox(lat, lon, 5)
        incidents = traffic_api.get_traffic_incidents(bbox)
        pois = traffic_api.search_poi(lat, lon, 2000)
        
        # Generate mobility insights
        patterns = data_processor.generate_mobility_patterns(
            traffic_flow, 
            incidents,
            pois
        )
        
        return jsonify(format_api_response(True, data={
            'location': {'lat': lat, 'lon': lon},
            'patterns': patterns,
            'data_sources': {
                'traffic_flow': bool(traffic_flow),
                'incidents': len(incidents),
                'pois': len(pois)
            }
        })), 200
        
    except Exception as e:
        logger.error(f"Error in get_mobility_patterns: {e}")
        return jsonify(format_api_response(False, error=str(e))), 500

@insights_bp.route('/area-classification', methods=['GET'])
def get_area_classification():
    """
    Classify urban area based on characteristics
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        # Validate coordinates
        valid, error = validate_coordinates(lat, lon)
        if not valid:
            return jsonify(format_api_response(False, error=error)), 400
        
        # Get data for classification
        pois = traffic_api.search_poi(lat, lon, 2000)
        traffic_flow = traffic_api.get_traffic_flow(lat, lon)
        
        # Classify the area
        classification = data_processor.classify_area(pois, traffic_flow)
        
        return jsonify(format_api_response(True, data={
            'location': {'lat': lat, 'lon': lon},
            'classification': classification
        })), 200
        
    except Exception as e:
        logger.error(f"Error in get_area_classification: {e}")
        return jsonify(format_api_response(False, error=str(e))), 500

@insights_bp.route('/test', methods=['GET'])
def test_insights():
    """Test endpoint"""
    return jsonify(format_api_response(True, data={
        'message': 'Insights service is operational',
        'endpoints': [
            'GET /api/insights/traffic?lat=X&lon=Y',
            'GET /api/insights/busiest-hours?lat=X&lon=Y',
            'GET /api/insights/poi-analysis?lat=X&lon=Y&radius=5000',
            'GET /api/insights/mobility-patterns?lat=X&lon=Y',
            'GET /api/insights/area-classification?lat=X&lon=Y'
        ]
    })), 200