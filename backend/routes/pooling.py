"""
Pooling API endpoints
Handles ride sharing and driver registration
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

pooling_bp = Blueprint('pooling', __name__)

# In-memory storage for demo
drivers_db = {}
rides_db = {}

@pooling_bp.route('/rides', methods=['GET'])
@jwt_required()
def search_rides():
    """
    Search for available rides
    """
    try:
        from_location = request.args.get('from', '').lower()
        to_location = request.args.get('to', '').lower()
        date = request.args.get('date', '')
        
        print(f"Searching rides from {from_location} to {to_location} on {date}")
        
        # For demo purposes - return no rides to show the message
        return jsonify({
            'success': True,
            'message': 'Sorry no vehicle poolers for this path',
            'rides': [],
            'route_options': get_route_options(from_location, to_location)
        }), 200
        
    except Exception as e:
        print(f"Error searching rides: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to search rides'
        }), 500

@pooling_bp.route('/driver/register', methods=['POST'])
@jwt_required()
def register_driver():
    """
    Register a new driver
    """
    try:
        current_user_email = get_jwt_identity()
        data = request.get_json()
        
        required_fields = [
            'full_name', 'dob', 'phone', 'aadhaar', 'pan', 
            'dl_number', 'dl_validity', 'rc_number', 'vehicle_type',
            'vehicle_make', 'vehicle_model', 'vehicle_year'
        ]
        
        # Validate required fields
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Store driver information
        driver_id = f"driver_{len(drivers_db) + 1}"
        drivers_db[driver_id] = {
            'id': driver_id,
            'user_email': current_user_email,
            **data,
            'registration_date': datetime.datetime.utcnow().isoformat(),
            'status': 'verified'
        }
        
        print(f"Driver registered: {data['full_name']}")
        
        return jsonify({
            'success': True,
            'message': 'Registered and verified as driver',
            'driver_id': driver_id,
            'status': 'verified'
        }), 201
        
    except Exception as e:
        print(f"Error registering driver: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to register driver'
        }), 500

def get_route_options(origin, destination):
    """
    Get three route options for the given origin and destination
    """
    # Mock route data - in production, this would call your routing engine
    return {
        'fastest_route': {
            'name': 'Fastest Route',
            'description': 'Uses real-time traffic analysis to get you there quickly',
            'duration': '2 hours 15 mins',
            'distance': '145 km',
            'traffic_conditions': 'Moderate traffic expected',
            'advantages': ['Quickest arrival', 'Real-time traffic updates']
        },
        'cheapest_route': {
            'name': 'Cheapest Route',
            'description': 'Optimized for fuel and toll costs to save you money',
            'duration': '2 hours 45 mins',
            'distance': '138 km',
            'cost_savings': 'Save ~₹250 compared to fastest route',
            'advantages': ['Lowest cost', 'Fuel efficient']
        },
        'eco_friendly_route': {
            'name': 'Eco-Friendly Route',
            'description': 'Designed to reduce carbon emissions and environmental impact',
            'duration': '2 hours 30 mins',
            'distance': '142 km',
            'carbon_reduction': '15% less emissions',
            'advantages': ['Environmentally friendly', 'Scenic routes']
        }
    }

@pooling_bp.route('/test', methods=['GET'])
def test_pooling():
    """Test endpoint"""
    return jsonify({
        'success': True,
        'message': 'Pooling service is operational',
        'endpoints': [
            'GET /api/pooling/rides?from=X&to=Y&date=Z',
            'POST /api/pooling/driver/register'
        ]
    }), 200