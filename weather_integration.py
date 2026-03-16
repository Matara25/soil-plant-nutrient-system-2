"""
Weather Integration Module for SoilDoctor System
Integrates Open-Meteo API for real-time weather data
"""

import requests
from datetime import datetime
import json

class WeatherAPI:
    """Weather API integration for SoilDoctor system"""
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.api_key = None  # Open-Meteo doesn't require API key for basic usage
        
    def get_current_weather(self, latitude, longitude):
        """
        Get current weather data for specific coordinates
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            dict: Weather data including temperature, wind speed, humidity
        """
        try:
            # Build API URL with parameters
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current_weather': 'true',
                'hourly': 'temperature_2m,relativehumidity_2m,windspeed_10m',
                'timezone': 'auto'
            }
            
            # Make API request
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract current weather data
                current = data.get('current_weather', {})
                hourly = data.get('hourly', {})
                
                # Get current hour index
                current_time = datetime.now().isoformat()
                
                weather_data = {
                    'location': {
                        'latitude': latitude,
                        'longitude': longitude
                    },
                    'current_weather': {
                        'temperature': current.get('temperature', 0),
                        'windspeed': current.get('windspeed', 0),
                        'winddirection': current.get('winddirection', 0),
                        'weather_code': current.get('weathercode', 0),
                        'is_day': current.get('is_day', 1)
                    },
                    'hourly_data': {
                        'temperature_2m': hourly.get('temperature_2m', []),
                        'relativehumidity_2m': hourly.get('relativehumidity_2m', []),
                        'windspeed_10m': hourly.get('windspeed_10m', []),
                        'time': hourly.get('time', [])
                    },
                    'timestamp': current_time,
                    'status': 'success'
                }
                
                return weather_data
            else:
                return {
                    'location': {'latitude': latitude, 'longitude': longitude},
                    'error': f'API request failed with status {response.status_code}',
                    'status': 'error'
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'location': {'latitude': latitude, 'longitude': longitude},
                'error': f'Request failed: {str(e)}',
                'status': 'error'
            }
        except Exception as e:
            return {
                'location': {'latitude': latitude, 'longitude': longitude},
                'error': f'Unexpected error: {str(e)}',
                'status': 'error'
            }
    
    def get_weather_forecast(self, latitude, longitude, days=7):
        """
        Get weather forecast for specific coordinates
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            days (int): Number of days to forecast (default: 7)
            
        Returns:
            dict: Weather forecast data
        """
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,weathercode',
                'timezone': 'auto',
                'forecast_days': days
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                daily = data.get('daily', {})
                
                forecast_data = {
                    'location': {'latitude': latitude, 'longitude': longitude},
                    'forecast': {
                        'time': daily.get('time', []),
                        'temperature_max': daily.get('temperature_2m_max', []),
                        'temperature_min': daily.get('temperature_2m_min', []),
                        'precipitation': daily.get('precipitation_sum', []),
                        'windspeed_max': daily.get('windspeed_10m_max', []),
                        'weather_code': daily.get('weathercode', [])
                    },
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success'
                }
                
                return forecast_data
            else:
                return {
                    'location': {'latitude': latitude, 'longitude': longitude},
                    'error': f'API request failed with status {response.status_code}',
                    'status': 'error'
                }
                
        except Exception as e:
            return {
                'location': {'latitude': latitude, 'longitude': longitude},
                'error': f'Forecast error: {str(e)}',
                'status': 'error'
            }
    
    def analyze_weather_for_agriculture(self, latitude, longitude):
        """
        Analyze weather data for agricultural recommendations
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            dict: Agricultural weather analysis
        """
        weather = self.get_current_weather(latitude, longitude)
        
        if weather['status'] != 'success':
            return weather
        
        current_temp = weather['current_weather']['temperature']
        wind_speed = weather['current_weather']['windspeed']
        
        # Agricultural analysis
        analysis = {
            'location': weather['location'],
            'current_conditions': weather['current_weather'],
            'agricultural_analysis': {
                'temperature_status': self._analyze_temperature(current_temp),
                'wind_status': self._analyze_wind(wind_speed),
                'irrigation_needs': self._analyze_irrigation_needs(weather),
                'field_work_conditions': self._analyze_field_conditions(weather)
            },
            'recommendations': self._get_agricultural_recommendations(weather),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return analysis
    
    def _analyze_temperature(self, temp):
        """Analyze temperature for agricultural purposes"""
        if temp < 10:
            return {"status": "cold", "risk": "frost", "recommendation": "Protect sensitive crops"}
        elif temp < 20:
            return {"status": "cool", "risk": "low", "recommendation": "Good for most crops"}
        elif temp < 30:
            return {"status": "optimal", "risk": "low", "recommendation": "Excellent growing conditions"}
        else:
            return {"status": "hot", "risk": "heat_stress", "recommendation": "Increase irrigation, provide shade"}
    
    def _analyze_wind(self, wind_speed):
        """Analyze wind conditions"""
        if wind_speed < 5:
            return {"status": "calm", "impact": "minimal", "recommendation": "Good for spraying"}
        elif wind_speed < 15:
            return {"status": "moderate", "impact": "normal", "recommendation": "Good field conditions"}
        else:
            return {"status": "strong", "impact": "high", "recommendation": "Avoid spraying, secure equipment"}
    
    def _analyze_irrigation_needs(self, weather):
        """Analyze irrigation requirements"""
        temp = weather['current_weather']['temperature']
        
        if temp > 25:
            return {"needs": "high", "reason": "High temperature increases evaporation"}
        elif temp > 15:
            return {"needs": "moderate", "reason": "Normal conditions"}
        else:
            return {"needs": "low", "reason": "Cool temperatures reduce evaporation"}
    
    def _analyze_field_conditions(self, weather):
        """Analyze suitability for field work"""
        temp = weather['current_weather']['temperature']
        wind = weather['current_weather']['windspeed']
        
        if 15 <= temp <= 30 and wind < 15:
            return {"suitability": "excellent", "activities": ["planting", "spraying", "harvesting"]}
        elif 10 <= temp <= 35 and wind < 20:
            return {"suitability": "good", "activities": ["light field work"]}
        else:
            return {"suitability": "poor", "activities": ["avoid field work"]}
    
    def _get_agricultural_recommendations(self, weather):
        """Get agricultural recommendations based on weather"""
        recommendations = []
        
        temp = weather['current_weather']['temperature']
        wind = weather['current_weather']['windspeed']
        
        if temp > 30:
            recommendations.append("Increase irrigation frequency")
            recommendations.append("Monitor for heat stress in crops")
        elif temp < 10:
            recommendations.append("Protect sensitive crops from frost")
            recommendations.append("Delay planting if possible")
        
        if wind > 15:
            recommendations.append("Avoid pesticide spraying")
            recommendations.append("Secure loose materials")
        
        if 15 <= temp <= 25 and wind < 10:
            recommendations.append("Optimal conditions for field operations")
            recommendations.append("Good time for fertilizer application")
        
        return recommendations

# Example usage and testing functions
def test_weather_api():
    """Test the weather API functionality"""
    weather_api = WeatherAPI()
    
    # Test coordinates (Nairobi, Kenya)
    lat, lon = -1.2921, 36.8219
    
    print("Testing Weather API...")
    print(f"Location: {lat}, {lon}")
    print("-" * 50)
    
    # Test current weather
    current = weather_api.get_current_weather(lat, lon)
    print("Current Weather:")
    print(json.dumps(current, indent=2))
    
    print("\n" + "-" * 50)
    
    # Test agricultural analysis
    analysis = weather_api.analyze_weather_for_agriculture(lat, lon)
    print("Agricultural Analysis:")
    print(json.dumps(analysis, indent=2))
    
    print("\n" + "-" * 50)
    
    # Test forecast
    forecast = weather_api.get_weather_forecast(lat, lon, days=3)
    print("3-Day Forecast:")
    print(json.dumps(forecast, indent=2))

if __name__ == "__main__":
    test_weather_api()
