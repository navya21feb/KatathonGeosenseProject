"""
ML prediction service
Uses trained models to predict traffic patterns
"""

import pickle
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

class MLPredictor:
    """Machine learning predictions for traffic patterns"""
    
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            # Initialize with a simple model if no saved model exists
            self._initialize_default_model()
    
    def load_model(self, model_path):
        """Load a trained ML model"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.is_trained = True
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self._initialize_default_model()
    
    def save_model(self, model_path):
        """Save the current model"""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler
            }
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            print("Model saved successfully")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def predict_traffic(self, features):
        """Predict traffic conditions"""
        if not self.is_trained:
            return self._default_prediction(features)
        
        try:
            # Prepare features for prediction
            feature_array = self._prepare_features(features)
            prediction = self.model.predict(feature_array)
            return self._interpret_prediction(prediction[0])
        except Exception as e:
            print(f"Error in traffic prediction: {e}")
            return self._default_prediction(features)
    
    def predict_busiest_hours(self, location, date):
        """Predict busiest hours for a location"""
        try:
            # Generate predictions for each hour of the day
            hours_predictions = []
            for hour in range(24):
                features = self._create_time_features(location, date, hour)
                traffic_level = self.predict_traffic(features)
                hours_predictions.append({
                    'hour': hour,
                    'traffic_level': traffic_level,
                    'congestion_percentage': self._traffic_to_percentage(traffic_level)
                })
            
            # Sort by congestion level
            hours_predictions.sort(key=lambda x: x['congestion_percentage'], reverse=True)
            
            return {
                'location': location,
                'date': date,
                'busiest_hours': hours_predictions[:3],  # Top 3 busiest hours
                'quietest_hours': hours_predictions[-3:][::-1],  # Top 3 quietest hours
                'daily_pattern': hours_predictions
            }
        except Exception as e:
            print(f"Error predicting busiest hours: {e}")
            return None
    
    def predict_route_time(self, route, time):
        """Predict travel time for a route"""
        try:
            base_time = route.get('travel_time', 0)
            
            # Adjust based on time of day and traffic predictions
            time_features = self._create_route_features(route, time)
            traffic_factor = self.predict_traffic(time_features)
            
            # Convert traffic level to time multiplier
            time_multiplier = self._traffic_to_time_multiplier(traffic_factor)
            predicted_time = base_time * time_multiplier
            
            return {
                'base_travel_time': base_time,
                'predicted_travel_time': predicted_time,
                'traffic_impact': round((time_multiplier - 1) * 100, 2),
                'confidence': self._calculate_confidence(time_features)
            }
        except Exception as e:
            print(f"Error predicting route time: {e}")
            return None
    
    def train_model(self, training_data):
        """Train the ML model with new data"""
        try:
            X = []
            y = []
            
            for data_point in training_data:
                features = self._extract_features(data_point)
                target = data_point['traffic_level']
                X.append(features)
                y.append(target)
            
            X_array = np.array(X)
            y_array = np.array(y)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X_array)
            
            # Train model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_scaled, y_array)
            self.is_trained = True
            
            print("Model trained successfully")
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def _initialize_default_model(self):
        """Initialize with a simple default model"""
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.is_trained = False
    
    def _prepare_features(self, features):
        """Prepare features for prediction"""
        feature_list = [
            features.get('hour_of_day', 12),
            features.get('day_of_week', 0),
            features.get('is_weekend', 0),
            features.get('month', 1),
            features.get('latitude', 0),
            features.get('longitude', 0),
            features.get('poi_density', 0),
            features.get('previous_traffic', 50)
        ]
        
        return self.scaler.transform([feature_list])
    
    def _create_time_features(self, location, date, hour):
        """Create features for time-based prediction"""
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        
        return {
            'hour_of_day': hour,
            'day_of_week': date_obj.weekday(),
            'is_weekend': 1 if date_obj.weekday() >= 5 else 0,
            'month': date_obj.month,
            'latitude': location['lat'],
            'longitude': location['lon'],
            'poi_density': self._estimate_poi_density(location),
            'previous_traffic': 50  # Default value
        }
    
    def _create_route_features(self, route, time):
        """Create features for route prediction"""
        time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        
        return {
            'hour_of_day': time_obj.hour,
            'day_of_week': time_obj.weekday(),
            'is_weekend': 1 if time_obj.weekday() >= 5 else 0,
            'month': time_obj.month,
            'latitude': route.get('start_lat', 0),
            'longitude': route.get('start_lon', 0),
            'poi_density': self._estimate_poi_density({
                'lat': route.get('start_lat', 0),
                'lon': route.get('start_lon', 0)
            }),
            'previous_traffic': route.get('historical_congestion', 50)
        }
    
    def _estimate_poi_density(self, location):
        """Estimate POI density around location (simplified)"""
        # In real implementation, this would use actual POI data
        # For now, return a simulated value based on urban/rural assumption
        return 75  # Default medium density
    
    def _interpret_prediction(self, prediction):
        """Convert numerical prediction to traffic level"""
        if prediction < 25:
            return 'very_light'
        elif prediction < 50:
            return 'light'
        elif prediction < 75:
            return 'moderate'
        elif prediction < 90:
            return 'heavy'
        else:
            return 'very_heavy'
    
    def _traffic_to_percentage(self, traffic_level):
        """Convert traffic level to percentage"""
        levels = {
            'very_light': 20,
            'light': 40,
            'moderate': 60,
            'heavy': 80,
            'very_heavy': 95
        }
        return levels.get(traffic_level, 50)
    
    def _traffic_to_time_multiplier(self, traffic_level):
        """Convert traffic level to time multiplier"""
        multipliers = {
            'very_light': 0.8,
            'light': 0.9,
            'moderate': 1.0,
            'heavy': 1.3,
            'very_heavy': 1.7
        }
        return multipliers.get(traffic_level, 1.0)
    
    def _calculate_confidence(self, features):
        """Calculate prediction confidence"""
        # Simplified confidence calculation
        base_confidence = 0.7
        # Increase confidence for more common scenarios
        if 7 <= features['hour_of_day'] <= 9 or 17 <= features['hour_of_day'] <= 19:
            base_confidence += 0.2  # Rush hours are more predictable
        return min(0.95, base_confidence)
    
    def _default_prediction(self, features):
        """Provide default prediction when model is not trained"""
        hour = features.get('hour_of_day', 12)
        
        # Simple rule-based prediction
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            return 'heavy'
        elif 10 <= hour <= 16:
            return 'moderate'
        else:
            return 'light'
    
    def _extract_features(self, data_point):
        """Extract features from training data point"""
        return [
            data_point.get('hour_of_day', 12),
            data_point.get('day_of_week', 0),
            data_point.get('is_weekend', 0),
            data_point.get('month', 1),
            data_point.get('latitude', 0),
            data_point.get('longitude', 0),
            data_point.get('poi_density', 0),
            data_point.get('previous_traffic', 50)
        ]