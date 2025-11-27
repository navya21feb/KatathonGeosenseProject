"""
Traffic Data Collection Script
Collects real-time traffic data from TomTom API and saves to database/CSV
This script should be run periodically (e.g., via cron job) to collect historical data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.services.traffic_api import TrafficAPI
from backend.config import Config
import pandas as pd
from datetime import datetime
import time
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrafficDataCollector:
    """Collect traffic data from TomTom API"""
    
    def __init__(self, output_dir='data/raw'):
        self.traffic_api = TrafficAPI()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Optional: MongoDB connection for persistence
        try:
            self.mongo_client = MongoClient(Config.MONGODB_URI)
            self.db = self.mongo_client[Config.MONGODB_DB_NAME]
            self.collection = self.db['traffic_data']
            self.use_mongodb = True
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.warning(f"MongoDB not available: {e}. Using CSV only.")
            self.use_mongodb = False
    
    def collect_location_data(self, lat, lon, location_name="Unknown"):
        """
        Collect traffic data for a specific location
        """
        logger.info(f"Collecting data for {location_name} ({lat}, {lon})")
        
        # Get traffic flow
        flow_data = self.traffic_api.get_traffic_flow(lat, lon)
        
        if not flow_data or not flow_data.get('success'):
            logger.error(f"Failed to get traffic data for {location_name}")
            return None
        
        # Prepare data record
        record = {
            'timestamp': datetime.now().isoformat(),
            'location_name': location_name,
            'lat': lat,
            'lon': lon,
            'hour': datetime.now().hour,
            'day_of_week': datetime.now().weekday(),
            'is_weekend': 1 if datetime.now().weekday() >= 5 else 0,
            'current_speed': flow_data.get('current_speed', 0),
            'free_flow_speed': flow_data.get('free_flow_speed', 0),
            'current_travel_time': flow_data.get('current_travel_time', 0),
            'free_flow_travel_time': flow_data.get('free_flow_travel_time', 0),
            'congestion_level_raw': flow_data.get('congestion_level', 'unknown'),
            'confidence': flow_data.get('confidence', 0)
        }
        
        # Calculate numeric congestion level
        if record['free_flow_speed'] > 0:
            record['congestion_level'] = 1 - (record['current_speed'] / record['free_flow_speed'])
            record['congestion_level'] = max(0, min(1, record['congestion_level']))  # Clip to [0,1]
        else:
            record['congestion_level'] = 0.5  # Default
        
        return record
    
    def collect_area_data(self, locations):
        """
        Collect data for multiple locations
        
        locations: list of dicts with 'lat', 'lon', 'name'
        """
        collected_data = []
        
        for location in locations:
            try:
                record = self.collect_location_data(
                    location['lat'],
                    location['lon'],
                    location.get('name', 'Unknown')
                )
                
                if record:
                    collected_data.append(record)
                    
                    # Save to MongoDB if available
                    if self.use_mongodb:
                        self.collection.insert_one(record.copy())
                        logger.info(f"Saved to MongoDB: {location['name']}")
                    
                # Rate limiting - be nice to the API
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error collecting data for {location['name']}: {e}")
        
        return collected_data
    
    def save_to_csv(self, data, filename=None):
        """
        Save collected data to CSV
        """
        if not data:
            logger.warning("No data to save")
            return
        
        df = pd.DataFrame(data)
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"traffic_data_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Append to existing file if it exists
        if os.path.exists(filepath):
            existing_df = pd.read_csv(filepath)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_csv(filepath, index=False)
        logger.info(f"Saved {len(df)} records to {filepath}")
        
        return filepath
    
    def collect_continuous(self, locations, interval_minutes=5, duration_hours=1):
        """
        Collect data continuously for a specified duration
        
        interval_minutes: how often to collect data
        duration_hours: how long to run the collection
        """
        logger.info(f"Starting continuous collection for {duration_hours} hours")
        logger.info(f"Collecting data every {interval_minutes} minutes")
        
        start_time = time.time()
        end_time = start_time + (duration_hours * 3600)
        
        all_data = []
        iteration = 0
        
        while time.time() < end_time:
            iteration += 1
            logger.info(f"\n--- Iteration {iteration} ---")
            
            # Collect data
            data = self.collect_area_data(locations)
            all_data.extend(data)
            
            # Save periodically
            if len(all_data) >= 50:  # Save every 50 records
                self.save_to_csv(all_data, filename='traffic_data_continuous.csv')
                all_data = []  # Clear buffer after saving
            
            # Wait for next iteration
            logger.info(f"Waiting {interval_minutes} minutes until next collection...")
            time.sleep(interval_minutes * 60)
        
        # Save any remaining data
        if all_data:
            self.save_to_csv(all_data, filename='traffic_data_continuous.csv')
        
        logger.info("Continuous collection completed!")

def get_delhi_locations():
    """
    Define key locations in Delhi for data collection
    """
    return [
        {'lat': 28.6139, 'lon': 77.2090, 'name': 'India Gate'},
        {'lat': 28.6304, 'lon': 77.2177, 'name': 'Connaught Place'},
        {'lat': 28.5355, 'lon': 77.3910, 'name': 'Noida Sector 18'},
        {'lat': 28.5494, 'lon': 77.2499, 'name': 'Nehru Place'},
        {'lat': 28.5244, 'lon': 77.1855, 'name': 'Saket'},
        {'lat': 28.7041, 'lon': 77.1025, 'name': 'Rohini'},
        {'lat': 28.6692, 'lon': 77.4538, 'name': 'Ghaziabad'},
        {'lat': 28.4595, 'lon': 77.0266, 'name': 'Gurugram Cyber Hub'},
        {'lat': 28.6517, 'lon': 77.2219, 'name': 'Kashmere Gate'},
        {'lat': 28.6507, 'lon': 77.2334, 'name': 'Chandni Chowk'}
    ]

def main():
    """
    Main execution
    """
    print("=" * 80)
    print("GeoSense Traffic Data Collection")
    print("=" * 80)
    
    # Initialize collector
    collector = TrafficDataCollector()
    
    # Get locations
    locations = get_delhi_locations()
    
    # Choose collection mode
    print("\nCollection Modes:")
    print("1. Single collection (collect once)")
    print("2. Continuous collection (collect periodically)")
    
    mode = input("\nSelect mode (1 or 2): ").strip()
    
    if mode == '1':
        # Single collection
        print("\nCollecting data for all locations...")
        data = collector.collect_area_data(locations)
        
        if data:
            filepath = collector.save_to_csv(data)
            print(f"\n✅ Data collection completed!")
            print(f"Collected {len(data)} records")
            print(f"Saved to: {filepath}")
        else:
            print("❌ No data collected")
    
    elif mode == '2':
        # Continuous collection
        interval = int(input("Collection interval in minutes (default 5): ") or "5")
        duration = int(input("Duration in hours (default 1): ") or "1")
        
        collector.collect_continuous(locations, interval_minutes=interval, duration_hours=duration)
    
    else:
        print("Invalid mode selected")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()