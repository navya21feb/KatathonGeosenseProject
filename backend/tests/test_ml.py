"""
Unit tests for ML prediction service
"""

import unittest
from services.ml_predictor import MLPredictor
import numpy as np

class TestMLPredictor(unittest.TestCase):
    """Test ML prediction service"""
    
    def setUp(self):
        self.predictor = MLPredictor()
    
    def test_traffic_prediction(self):
        """Test traffic prediction"""
        features = {
            'hour_of_day': 8,
            'day_of_week': 0,
            'is_weekend': 0,
            'month': 1,
            'latitude': 12.34,
            'longitude': 56.78,
            'poi_density': 75,
            'previous_traffic': 50
        }
        
        prediction = self.predictor.predict_traffic(features)
        self.assertIn(prediction, ['very_light', 'light', 'moderate', 'heavy', 'very_heavy'])
    
    def test_busiest_hours_prediction(self):
        """Test busiest hours prediction"""
        location = {'lat': 12.34, 'lon': 56.78}
        date = '2024-01-01'
        
        result = self.predictor.predict_busiest_hours(location, date)
        self.assertIsNotNone(result)
        self.assertIn('busiest_hours', result)
        self.assertIn('quietest_hours', result)
    
    def test_route_time_prediction(self):
        """Test route time prediction"""
        route = {
            'travel_time': 1800,
            'start_lat': 12.34,
            'start_lon': 56.78,
            'historical_congestion': 60
        }
        time = '2024-01-01 08:00:00'
        
        result = self.predictor.predict_route_time(route, time)
        self.assertIsNotNone(result)
        self.assertIn('predicted_travel_time', result)
        self.assertIn('traffic_impact', result)

if __name__ == '__main__':
    unittest.main()