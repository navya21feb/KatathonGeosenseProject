"""
Routing API endpoints - FIXED VERSION
Handles route calculation for fastest, cheapest, and eco-friendly routes
"""

from flask import Blueprint, jsonify, request
from services.routing_engine import RoutingEngine
from utils.helpers import format_api_response
from utils.validators import validate_route_params
import logging

logger = logging.getLogger(__name__)
routing_bp = Blueprint('routing', __name__)
routing_engine = RoutingEngine()

@routing_bp.route('/compare', methods=['POST'])
def compare_routes():
    """
    Compare three routes: fastest, cheapest, eco-friendly
    """
    try:
        data = request.get_json()
        
        # Validate input
        valid, error = validate_route_params(data)
        if not valid:
            return jsonify(format_api_response(False, error=error)), 400
        
        origin = data['origin']
        destination = data['destination']
        
        # Compare all routes
        comparison = routing_engine.compare_routes(origin, destination)
        
        if not comparison:
            return jsonify(format_api_response(False, error="Route calculation failed")), 500
        
        return jsonify(format_api_response(True, data=comparison)), 200
            
    except Exception as e:
        import traceback
        logger.error(f"Error in compare_routes: {e}")
        traceback.print_exc()
        return jsonify(format_api_response(False, error=str(e))), 500

@routing_bp.route('/fastest', methods=['POST'])
def get_fastest_route():
    """
    Get the fastest route between two points
    """
    try:
        data = request.get_json()
        
        # Validate input
        valid, error = validate_route_params(data)
        if not valid:
            return jsonify(format_api_response(False, error=error)), 400
        
        origin = data['origin']
        destination = data['destination']
        
        route = routing_engine.calculate_fastest_route(origin, destination)
        
        if not route:
            return jsonify(format_api_response(False, error="Fastest route calculation failed")), 500
        
        return jsonify(format_api_response(True, data=route)), 200
            
    except Exception as e:
        logger.error(f"Error in get_fastest_route: {e}")
        return jsonify(format_api_response(False, error=str(e))), 500

@routing_bp.route('/cheapest', methods=['POST'])
def get_cheapest_route():
    """
    Get the cheapest route between two points
    """
    try:
        data = request.get_json()
        
        # Validate input
        valid, error = validate_route_params(data)
        if not valid:
            return jsonify(format_api_response(False, error=error)), 400
        
        origin = data['origin']
        destination = data['destination']
        
        route = routing_engine.calculate_cheapest_route(origin, destination)
        
        if not route:
            return jsonify(format_api_response(False, error="Cheapest route calculation failed")), 500
        
        return jsonify(format_api_response(True, data=route)), 200
            
    except Exception as e:
        logger.error(f"Error in get_cheapest_route: {e}")
        return jsonify(format_api_response(False, error=str(e))), 500

@routing_bp.route('/eco-friendly', methods=['POST'])
def get_eco_route():
    """
    Get the most eco-friendly route between two points
    """
    try:
        data = request.get_json()
        
        # Validate input
        valid, error = validate_route_params(data)
        if not valid:
            return jsonify(format_api_response(False, error=error)), 400
        
        origin = data['origin']
        destination = data['destination']
        
        route = routing_engine.calculate_eco_route(origin, destination)
        
        if not route:
            return jsonify(format_api_response(False, error="Eco-friendly route calculation failed")), 500
        
        return jsonify(format_api_response(True, data=route)), 200
            
    except Exception as e:
        logger.error(f"Error in get_eco_route: {e}")
        return jsonify(format_api_response(False, error=str(e))), 500

@routing_bp.route('/test', methods=['GET'])
def test_routing():
    """Test endpoint"""
    return jsonify(format_api_response(True, data={
        'message': 'Routing service is operational',
        'endpoints': [
            'POST /api/routing/compare',
            'POST /api/routing/fastest', 
            'POST /api/routing/cheapest',
            'POST /api/routing/eco-friendly'
        ]
    })), 200