"""
Routing API endpoints
Handles route calculation for fastest, cheapest, and eco-friendly routes
"""

from flask import Blueprint, jsonify, request
from services.routing_engine import RoutingEngine
import logging

logger = logging.getLogger(__name__)
routing_bp = Blueprint('routing', __name__)
routing_engine = RoutingEngine()

@routing_bp.route('/compare', methods=['POST'])
def compare_routes():
    """
    Compare three routes: fastest, cheapest, eco-friendly
    
    Expected JSON body:
    {
        "origin": {"lat": 28.6139, "lon": 77.2090},
        "destination": {"lat": 28.5355, "lon": 77.3910}
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'origin' not in data or 'destination' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing origin or destination'
            }), 400
        
        origin = data['origin']
        destination = data['destination']
        
        # Validate coordinates
        if not all(k in origin for k in ['lat', 'lon']) or \
           not all(k in destination for k in ['lat', 'lon']):
            return jsonify({
                'success': False,
                'error': 'Invalid coordinates format. Required: {lat, lon}'
            }), 400
        
        # Convert to list format
        origin_coords = [origin['lat'], origin['lon']]
        destination_coords = [destination['lat'], destination['lon']]
        
        # Calculate all routes
        result = routing_engine.compare_routes(origin_coords, destination_coords)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in compare_routes: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@routing_bp.route('/fastest', methods=['POST'])
def get_fastest_route():
    """
    Get the fastest route between two points
    
    Expected JSON body:
    {
        "origin": {"lat": 28.6139, "lon": 77.2090},
        "destination": {"lat": 28.5355, "lon": 77.3910}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'origin' not in data or 'destination' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing origin or destination'
            }), 400
        
        origin = [data['origin']['lat'], data['origin']['lon']]
        destination = [data['destination']['lat'], data['destination']['lon']]
        
        result = routing_engine.calculate_fastest_route(origin, destination)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in get_fastest_route: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@routing_bp.route('/cheapest', methods=['POST'])
def get_cheapest_route():
    """
    Get the cheapest route between two points
    Avoids tolls and uses shortest distance
    
    Expected JSON body:
    {
        "origin": {"lat": 28.6139, "lon": 77.2090},
        "destination": {"lat": 28.5355, "lon": 77.3910}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'origin' not in data or 'destination' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing origin or destination'
            }), 400
        
        origin = [data['origin']['lat'], data['origin']['lon']]
        destination = [data['destination']['lat'], data['destination']['lon']]
        
        result = routing_engine.calculate_cheapest_route(origin, destination)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in get_cheapest_route: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@routing_bp.route('/eco-friendly', methods=['POST'])
def get_eco_route():
    """
    Get the most eco-friendly route between two points
    Optimizes for fuel efficiency and lower emissions
    
    Expected JSON body:
    {
        "origin": {"lat": 28.6139, "lon": 77.2090},
        "destination": {"lat": 28.5355, "lon": 77.3910}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'origin' not in data or 'destination' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing origin or destination'
            }), 400
        
        origin = [data['origin']['lat'], data['origin']['lon']]
        destination = [data['destination']['lat'], data['destination']['lon']]
        
        result = routing_engine.calculate_eco_route(origin, destination)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in get_eco_route: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@routing_bp.route('/test', methods=['GET'])
def test_routing():
    """Test endpoint to verify routing service is working"""
    return jsonify({
        'success': True,
        'message': 'Routing service is operational',
        'available_endpoints': [
            'POST /api/routing/compare',
            'POST /api/routing/fastest',
            'POST /api/routing/cheapest',
            'POST /api/routing/eco-friendly'
        ]
    }), 200