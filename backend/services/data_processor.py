"""
Data processor service
Handles data aggregation, analysis, and pattern generation
"""

from datetime import datetime
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Process and analyze traffic and POI data"""
    
    @staticmethod
    def analyze_busiest_hours(lat, lon, current_traffic):
        """
        Analyze and predict busiest hours based on current traffic patterns
        In production, this would use historical data from database
        """
        current_hour = datetime.now().hour
        congestion = current_traffic.get('congestion_level', 'unknown')
        
        # Typical urban traffic patterns
        patterns = {
            'weekday': [
                {'hour': 0, 'congestion': 'low', 'avg_speed_reduction': 0},
                {'hour': 1, 'congestion': 'low', 'avg_speed_reduction': 0},
                {'hour': 2, 'congestion': 'low', 'avg_speed_reduction': 0},
                {'hour': 3, 'congestion': 'low', 'avg_speed_reduction': 0},
                {'hour': 4, 'congestion': 'low', 'avg_speed_reduction': 5},
                {'hour': 5, 'congestion': 'moderate', 'avg_speed_reduction': 10},
                {'hour': 6, 'congestion': 'moderate', 'avg_speed_reduction': 20},
                {'hour': 7, 'congestion': 'high', 'avg_speed_reduction': 35},
                {'hour': 8, 'congestion': 'high', 'avg_speed_reduction': 40},
                {'hour': 9, 'congestion': 'moderate', 'avg_speed_reduction': 25},
                {'hour': 10, 'congestion': 'moderate', 'avg_speed_reduction': 15},
                {'hour': 11, 'congestion': 'moderate', 'avg_speed_reduction': 15},
                {'hour': 12, 'congestion': 'moderate', 'avg_speed_reduction': 20},
                {'hour': 13, 'congestion': 'moderate', 'avg_speed_reduction': 15},
                {'hour': 14, 'congestion': 'moderate', 'avg_speed_reduction': 15},
                {'hour': 15, 'congestion': 'moderate', 'avg_speed_reduction': 20},
                {'hour': 16, 'congestion': 'high', 'avg_speed_reduction': 30},
                {'hour': 17, 'congestion': 'high', 'avg_speed_reduction': 40},
                {'hour': 18, 'congestion': 'high', 'avg_speed_reduction': 45},
                {'hour': 19, 'congestion': 'moderate', 'avg_speed_reduction': 30},
                {'hour': 20, 'congestion': 'moderate', 'avg_speed_reduction': 20},
                {'hour': 21, 'congestion': 'low', 'avg_speed_reduction': 10},
                {'hour': 22, 'congestion': 'low', 'avg_speed_reduction': 5},
                {'hour': 23, 'congestion': 'low', 'avg_speed_reduction': 0}
            ]
        }
        
        hourly_data = patterns['weekday']
        
        # Find peak hours
        peak_hours = [h for h in hourly_data if h['congestion'] == 'high']
        quiet_hours = [h for h in hourly_data if h['congestion'] == 'low']
        
        return {
            'hourly_breakdown': hourly_data,
            'peak_hours': [h['hour'] for h in peak_hours],
            'quiet_hours': [h['hour'] for h in quiet_hours],
            'current_hour': current_hour,
            'current_status': congestion,
            'recommendations': {
                'best_time_to_travel': f"Between {quiet_hours[0]['hour']}:00 - {quiet_hours[-1]['hour']}:00 for minimal traffic",
                'avoid_hours': f"Avoid {peak_hours[0]['hour']}:00 - {peak_hours[-1]['hour']}:00 (peak traffic)"
            }
        }
    
    @staticmethod
    def analyze_poi_distribution(pois):
        """Analyze POI distribution and generate insights"""
        if not pois:
            return {
                'total_pois': 0,
                'categories': {},
                'insights': ['No POIs found in this area']
            }
        
        # Count POIs by category
        categories = Counter([poi.get('category', 'Unknown') for poi in pois])
        
        # Calculate average distances
        distances = [poi.get('distance', 0) for poi in pois if poi.get('distance')]
        avg_distance = sum(distances) / len(distances) if distances else 0
        
        # Generate insights
        insights = []
        top_category = categories.most_common(1)[0] if categories else None
        
        if top_category:
            insights.append(f"Area dominated by {top_category[0]} ({top_category[1]} locations)")
        
        if avg_distance < 500:
            insights.append("High POI density - urban commercial area")
        elif avg_distance < 2000:
            insights.append("Moderate POI density - mixed-use area")
        else:
            insights.append("Low POI density - residential or suburban area")
        
        return {
            'total_pois': len(pois),
            'categories': dict(categories),
            'avg_distance_meters': round(avg_distance, 2),
            'insights': insights,
            'top_categories': categories.most_common(5)
        }
    
    @staticmethod
    def generate_mobility_patterns(traffic_flow, incidents, pois):
        """Generate comprehensive mobility patterns from multiple data sources"""
        patterns = {
            'congestion_status': traffic_flow.get('congestion_level', 'unknown'),
            'incident_impact': 'high' if len(incidents) > 5 else 'low' if len(incidents) > 0 else 'none',
            'area_activity': 'high' if len(pois) > 50 else 'moderate' if len(pois) > 20 else 'low'
        }
        
        # Generate area description
        congestion = patterns['congestion_status']
        activity = patterns['area_activity']
        
        descriptions = []
        
        if congestion in ['high', 'severe']:
            descriptions.append("Heavy traffic congestion expected")
        elif congestion == 'moderate':
            descriptions.append("Moderate traffic flow")
        else:
            descriptions.append("Smooth traffic conditions")
        
        if activity == 'high':
            descriptions.append("High commercial activity area")
        elif activity == 'moderate':
            descriptions.append("Mixed-use area with moderate activity")
        else:
            descriptions.append("Quiet residential or suburban area")
        
        if len(incidents) > 0:
            descriptions.append(f"{len(incidents)} active traffic incidents affecting mobility")
        
        patterns['description'] = '. '.join(descriptions)
        patterns['mobility_score'] = DataProcessor._calculate_mobility_score(
            congestion, len(incidents), activity
        )
        
        return patterns
    
    @staticmethod
    def classify_area(pois, traffic_flow):
        """Classify an area based on POIs and traffic patterns"""
        if not pois:
            return {
                'primary_type': 'Unknown',
                'characteristics': [],
                'suitable_for': []
            }
        
        # Count POI categories
        categories = Counter([poi.get('category', 'Unknown') for poi in pois])
        top_categories = [cat[0] for cat in categories.most_common(3)]
        
        # Determine area type
        area_type = 'Mixed-use'
        characteristics = []
        suitable_for = []
        
        # Commercial indicators
        commercial_keywords = ['shop', 'restaurant', 'store', 'mall', 'retail']
        if any(keyword in ' '.join(top_categories).lower() for keyword in commercial_keywords):
            area_type = 'Commercial Hub'
            characteristics.append('High retail density')
            suitable_for.append('Shopping and dining')
        
        # Office/Business indicators
        office_keywords = ['office', 'business', 'corporate']
        if any(keyword in ' '.join(top_categories).lower() for keyword in office_keywords):
            area_type = 'Business District'
            characteristics.append('Professional offices')
            suitable_for.append('Business meetings')
        
        # Residential indicators
        residential_keywords = ['residential', 'housing', 'apartment']
        if any(keyword in ' '.join(top_categories).lower() for keyword in residential_keywords):
            area_type = 'Residential Zone'
            characteristics.append('Primarily residential')
            suitable_for.append('Quiet living')
        
        # Entertainment indicators
        entertainment_keywords = ['entertainment', 'cinema', 'theatre', 'bar', 'nightclub']
        if any(keyword in ' '.join(top_categories).lower() for keyword in entertainment_keywords):
            area_type = 'Entertainment District'
            characteristics.append('Active nightlife')
            suitable_for.append('Evening entertainment')
        
        # Add traffic characteristics
        congestion = traffic_flow.get('congestion_level', 'unknown')
        if congestion in ['low']:
            characteristics.append('Low traffic - quiet area')
            suitable_for.append('Evening walks')
        elif congestion in ['high', 'severe']:
            characteristics.append('High traffic - busy area')
        
        return {
            'primary_type': area_type,
            'characteristics': characteristics,
            'suitable_for': suitable_for,
            'dominant_categories': top_categories,
            'traffic_level': congestion,
            'poi_count': len(pois)
        }
    
    @staticmethod
    def _calculate_mobility_score(congestion, incident_count, activity_level):
        """Calculate a mobility score (0-100, higher is better)"""
        score = 100
        
        # Deduct for congestion
        if congestion == 'severe':
            score -= 40
        elif congestion == 'high':
            score -= 30
        elif congestion == 'moderate':
            score -= 15
        
        # Deduct for incidents
        score -= min(incident_count * 5, 30)
        
        # Slight deduction for very high activity (crowded)
        if activity_level == 'high':
            score -= 5
        
        return max(0, score)