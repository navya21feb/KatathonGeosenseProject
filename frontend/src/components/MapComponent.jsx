import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./MapComponent.css";

// Fix marker issue for Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

// Custom icon for user location
const userLocationIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Component to handle map centering when location changes
function MapCenterHandler({ center }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, map.getZoom());
  }, [center, map]);
  return null;
}

// Load key from .env
const API_KEY = import.meta.env.VITE_TOMTOM_API_KEY;

const MapComponent = ({
  zoom = 13,
  markers = [],
  className = "",
  showUserLocation = true,
}) => {
  const [userLocation, setUserLocation] = useState(null);
  const [center, setCenter] = useState([28.6139, 77.2090]); // Default: Delhi
  const [locationStatus, setLocationStatus] = useState("idle"); // idle, loading, success, error
  const [locationError, setLocationError] = useState("");

  // Get user's current location
  const getUserLocation = () => {
    if (!navigator.geolocation) {
      setLocationError("Geolocation is not supported by this browser.");
      setLocationStatus("error");
      return;
    }

    setLocationStatus("loading");
    
    const options = {
      enableHighAccuracy: true,
      timeout: 10000, // 10 seconds
      maximumAge: 600000 // 10 minutes
    };

    navigator.geolocation.watchPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        const userCoords = [latitude, longitude];
        
        setUserLocation(userCoords);
        setCenter(userCoords);
        setLocationStatus("success");
        setLocationError("");
      },
      (error) => {
        console.error("Error getting location:", error);
        setLocationStatus("error");
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            setLocationError("Location access denied. Please enable location permissions in your browser.");
            break;
          case error.POSITION_UNAVAILABLE:
            setLocationError("Location information is unavailable.");
            break;
          case error.TIMEOUT:
            setLocationError("Location request timed out. Please try again.");
            break;
          default:
            setLocationError("An unknown error occurred while getting your location.");
            break;
        }
      },
      options
    );
  };

  // Auto-get location when component mounts
  useEffect(() => {
    if (showUserLocation) {
      getUserLocation();
    }
  }, [showUserLocation]);

  // Validate API key
  if (!API_KEY) {
    return (
      <div className="map-container error">
        <div className="error-message">
          <h3>Map Unavailable</h3>
          <p>TomTom API key is not configured.</p>
          <p>Please check your environment variables.</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`map-container ${className}`}>
      {/* Location Status Panel */}
      <div className="location-status">
        {locationStatus === "loading" && (
          <div className="status-loading">
            <span>📍 Getting your location...</span>
          </div>
        )}
        
        {locationStatus === "error" && (
          <div className="status-error">
            <span>❌ {locationError}</span>
            <button onClick={getUserLocation} className="retry-btn">
              Try Again
            </button>
          </div>
        )}
        
        {locationStatus === "success" && (
          <div className="status-success">
            <span>📍Showing your current location</span>
          </div>
        )}
      </div>

      <MapContainer 
        center={center} 
        zoom={zoom} 
        style={{ height: "100%", width: "100%" }}
        scrollWheelZoom={true}
      >
        <MapCenterHandler center={center} />
        
        {/* TomTom Tile Layer */}
        <TileLayer
          url={`https://api.tomtom.com/map/1/tile/basic/main/{z}/{x}/{y}.png?key=${API_KEY}&tileSize=256&view=Unified`}
          attribution='&copy; <a href="https://www.tomtom.com/copyright/" target="_blank">TomTom</a>'
          minZoom={0}
          maxZoom={22}
        />

        {/* User Location Marker */}
        {userLocation && (
          <Marker position={userLocation} icon={userLocationIcon}>
            <Popup>
              <div className="custom-popup">
                <h4>📍 Your Location</h4>
                <p>Lat: {userLocation[0].toFixed(6)}</p>
                <p>Lng: {userLocation[1].toFixed(6)}</p>
              </div>
            </Popup>
          </Marker>
        )}

        {/* Additional markers */}
        {markers.map((marker, index) => (
          <Marker key={index} position={marker.position}>
            {marker.popup && (
              <Popup>
                <div className="custom-popup">
                  {marker.popup}
                </div>
              </Popup>
            )}
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;