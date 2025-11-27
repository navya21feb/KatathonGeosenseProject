"""
Unit tests for routing endpoints
"""

import unittest
from app import create_app
from unittest.mock import patch, MagicMock

class TestRoutes(unittest.TestCase):
    """Test routing API endpoints"""
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    @patch('services.routing_engine.RoutingEngine.compare_routes')
    def test_route_comparison(self, mock_compare):
        """Test route comparison endpoint"""
        mock_compare.return_value = {
            'fastest_route': {'travel_time': 1800, 'distance': 15000},
            'cheapest_route': {'travel_time': 2100, 'total_cost': 150},
            'eco_friendly_route': {'travel_time': 2000, 'co2_emissions': 2.1}
        }
        
        response = self.client.post('/api/routes/compare',
                                  json={
                                      'origin': {'lat': 12.34, 'lon': 56.78},
                                      'destination': {'lat': 12.35, 'lon': 56.79}
                                  })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('fastest_route', data)
        self.assertIn('cheapest_route', data)
        self.assertIn('eco_friendly_route', data)
    
    @patch('services.routing_engine.RoutingEngine.calculate_fastest_route')
    def test_fastest_route(self, mock_fastest):
        """Test fastest route endpoint"""
        mock_fastest.return_value = {
            'type': 'fastest',
            'travel_time': 1800,
            'distance': 15000,
            'coordinates': []
        }
        
        response = self.client.post('/api/routes/fastest',
                                  json={
                                      'origin': {'lat': 12.34, 'lon': 56.78},
                                      'destination': {'lat': 12.35, 'lon': 56.79}
                                  })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['type'], 'fastest')

if __name__ == '__main__':
    unittest.main()