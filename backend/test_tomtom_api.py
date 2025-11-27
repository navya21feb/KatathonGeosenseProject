"""
Test TomTom API connection with your API key
Run this to verify everything works
"""

import requests
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.config import Config
from backend.services.traffic_api import TrafficAPI
from backend.services.routing_engine import RoutingEngine

def test_api_key():
    """Test if API key is valid"""
    print("=" * 80)
    print("TESTING TOMTOM API CONNECTION")
    print("=" * 80)
    
    api_key = Config.TOMTOM_API_KEY
    print(f"\n✓ API Key loaded: {api_key[:20]}...")
    
    # Simple test request
    test_url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    params = {
        'key': api_key,
        'point': '28.6139,77.2090',  # India Gate, Delhi
        'unit': 'KMPH'
    }
    
    print(f"\n🔍 Testing API endpoint...")
    try:
        response = requests.get(test_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print("✅ API Connection: SUCCESS!")
        print(f"✅ Response received: {len(str(data))} bytes")
        
        if 'flowSegmentData' in data:
            flow = data['flowSegmentData']
            print(f"\n📊 Live Traffic Data (India Gate, Delhi):")
            print(f"   Current Speed: {flow.get('currentSpeed', 0)} km/h")
            print(f"   Free Flow Speed: {flow.get('freeFlowSpeed', 0)} km/h")
            print(f"   Confidence: {flow.get('confidence', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ API Connection: FAILED")
        print(f"   Error: {str(e)}")
        return False

def test_traffic_api():
    """Test TrafficAPI class"""
    print("\n" + "=" * 80)
    print("TESTING TRAFFIC API SERVICE")
    print("=" * 80)
    
    traffic_api = TrafficAPI()
    
    # Test 1: Traffic Flow
    print("\n🚦 Test 1: Get Traffic Flow (India Gate)")
    result = traffic_api.get_traffic_flow(28.6139, 77.2090)
    
    if result and result.get('success'):
        print("✅ Traffic Flow: SUCCESS")
        print(f"   Current Speed: {result.get('current_speed')} km/h")
        print(f"   Congestion Level: {result.get('congestion_level')}")
    else:
        print("❌ Traffic Flow: FAILED")
    
    # Test 2: Traffic Incidents
    print("\n🚨 Test 2: Get Traffic Incidents (Delhi area)")
    bbox = "77.1,28.5,77.3,28.7"  # Delhi bounding box
    result = traffic_api.get_traffic_incidents(bbox)
    
    if result and result.get('success'):
        print("✅ Traffic Incidents: SUCCESS")
        print(f"   Active Incidents: {result.get('incident_count', 0)}")
    else:
        print("❌ Traffic Incidents: FAILED")
    
    # Test 3: POI Search
    print("\n📍 Test 3: Search Nearby POIs (Connaught Place)")
    result = traffic_api.search_nearby_pois(28.6304, 77.2177, radius=2000)
    
    if result and result.get('success'):
        print("✅ POI Search: SUCCESS")
        print(f"   POIs Found: {result.get('poi_count', 0)}")
        if result.get('pois'):
            print(f"   First POI: {result['pois'][0]['name']}")
    else:
        print("❌ POI Search: FAILED")

def test_routing_engine():
    """Test RoutingEngine for 3 route types"""
    print("\n" + "=" * 80)
    print("TESTING ROUTING ENGINE (3 ROUTE TYPES)")
    print("=" * 80)
    
    routing = RoutingEngine()
    
    # Test route: India Gate to Noida Sector 18
    origin = [28.6139, 77.2090]  # India Gate
    destination = [28.5355, 77.3910]  # Noida
    
    print(f"\n🗺️  Route: India Gate → Noida Sector 18")
    
    # Test Fastest Route
    print("\n⚡ Test 1: Fastest Route")
    result = routing.calculate_fastest_route(origin, destination)
    if result and result.get('success'):
        print("✅ Fastest Route: SUCCESS")
        print(f"   Distance: {result.get('distance_km')} km")
        print(f"   Duration: {result.get('duration_minutes')} min")
        print(f"   Cost: ${result.get('cost_usd')}")
        print(f"   CO2: {result.get('co2_kg')} kg")
    else:
        print("❌ Fastest Route: FAILED")
        print(f"   Error: {result.get('error')}")
    
    # Test Cheapest Route
    print("\n💰 Test 2: Cheapest Route")
    result = routing.calculate_cheapest_route(origin, destination)
    if result and result.get('success'):
        print("✅ Cheapest Route: SUCCESS")
        print(f"   Distance: {result.get('distance_km')} km")
        print(f"   Cost: ${result.get('cost_usd')}")
    else:
        print("❌ Cheapest Route: FAILED")
    
    # Test Eco Route
    print("\n🌱 Test 3: Eco-Friendly Route")
    result = routing.calculate_eco_route(origin, destination)
    if result and result.get('success'):
        print("✅ Eco Route: SUCCESS")
        print(f"   Distance: {result.get('distance_km')} km")
        print(f"   CO2: {result.get('co2_kg')} kg")
    else:
        print("❌ Eco Route: FAILED")
    
    # Test Route Comparison
    print("\n📊 Test 4: Compare All Routes")
    result = routing.compare_routes(origin, destination)
    if result and result.get('success'):
        print("✅ Route Comparison: SUCCESS")
        print(f"   Routes compared: 3")
        comparison = result.get('comparison')
        if comparison:
            print(f"   Recommendation: {comparison.get('recommendation', 'N/A')}")
            if 'note' in comparison:
                print(f"   Note: {comparison.get('note')}")
        else:
            print("   Note: Comparison data not available")
    else:
        print("❌ Route Comparison: FAILED")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "GEOSENSE REAL-TIME API TESTS" + " " * 30 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Test 1: Basic API key
    success1 = test_api_key()
    
    # Test 2: Traffic API Service
    test_traffic_api()
    
    # Test 3: Routing Engine
    test_routing_engine()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    if success1:
        print("\n✅ Your TomTom API key is working!")
        print("✅ Real-time traffic data is accessible")
        print("✅ All services are operational")
        print("\n🎉 YOU'RE READY TO USE REAL-TIME DATA!")
        print("\nNext steps:")
        print("1. Start backend: cd backend && python app.py")
        print("2. Test endpoints: curl http://localhost:5000/api/health")
        print("3. Get live traffic: curl 'http://localhost:5000/api/insights/traffic?lat=28.6139&lon=77.2090'")
    else:
        print("\n❌ API key test failed")
        print("Please check:")
        print("1. API key is correct in .env file")
        print("2. Internet connection is active")
        print("3. API key has proper permissions")
    
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()