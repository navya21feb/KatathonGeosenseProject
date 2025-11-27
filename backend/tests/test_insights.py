"""
Unit tests for insights endpoints
"""

import unittest
from app import create_app
from unittest.mock import patch, MagicMock

class TestInsights(unittest.TestCase):
    """Test insights API endpoints"""
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    @patch('services.traffic_api.TrafficAPI.get_traffic_flow')
    def test_traffic_insights_endpoint(self, mock_traffic_flow):
        """Test traffic insights endpoint"""
        mock_traffic_flow.return_value = {
            'current_speed': 45,
            'free_flow_speed': 60,
            'congestion_level': 25,
            'confidence': 0.8
        }
        
        response = self.client.get('/api/insights/traffic?lat=12.34&lon=56.78')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('congestion_level', data)
    
    @patch('services.ml_predictor.MLPredictor.predict_busiest_hours')
    def test_busiest_hours_endpoint(self, mock_predict):
        """Test busiest hours endpoint"""
        mock_predict.return_value = {
            'location': {'lat': 12.34, 'lon': 56.78},
            'date': '2024-01-01',
            'busiest_hours': [
                {'hour': 8, 'traffic_level': 'heavy', 'congestion_percentage': 85},
                {'hour': 18, 'traffic_level': 'heavy', 'congestion_percentage': 80}
            ]
        }
        
        response = self.client.post('/api/insights/busiest-hours', 
                                  json={'lat': 12.34, 'lon': 56.78, 'date': '2024-01-01'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('busiest_hours', data)

if __name__ == '__main__':
    unittest.main()