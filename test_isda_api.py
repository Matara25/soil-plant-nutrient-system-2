#!/usr/bin/env python3
"""
iSDA API Test Script
Test authentication and data fetching from iSDA Africa Soil API
"""

import requests
import json
from datetime import datetime

class ISDATest:
    """Test iSDA API functionality"""
    
    def __init__(self):
        self.base_url = "https://api.isda-africa.com"
        self.token = None
    
    def authenticate(self, email, password):
        """Authenticate with iSDA API"""
        try:
            print("🔐 Authenticating with iSDA API...")
            
            auth_url = f"{self.base_url}/login"
            headers = {
                "accept": "application/json"
            }
            payload = {
                "username": email,
                "password": password
            }
            
            response = requests.post(auth_url, headers=headers, data=payload)
            
            if response.status_code == 200:
                auth_data = response.json()
                self.token = auth_data.get('access_token')
                print(f"✅ Authentication successful!")
                print(f"📋 Token received: {self.token[:50]}...")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(f"📄 Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def test_soil_properties(self, lat=-1.2921, lon=36.8219):
        """Test soil properties endpoint"""
        if not self.token:
            print("❌ Not authenticated. Please authenticate first.")
            return None
        
        try:
            print(f"\n🌱 Testing soil properties for ({lat}, {lon})...")
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json"
            }
            
            soil_url = f"{self.base_url}/isdasoil/v2/soilproperty"
            params = {
                "lat": lat,
                "lon": lon
            }
            
            response = requests.get(soil_url, headers=headers, params=params)
            
            if response.status_code == 200:
                soil_data = response.json()
                print(f"✅ Soil data retrieved successfully!")
                
                # Display key information
                if 'property' in soil_data:
                    props = soil_data['property']
                    print(f"\n📊 Soil Properties Found:")
                    for key, value in list(props.items())[:5]:  # Show first 5 properties
                        if isinstance(value, list) and len(value) > 0:
                            item = value[0]
                            if 'value' in item:
                                print(f"  {key}: {item['value']}")
                            else:
                                print(f"  {key}: {item}")
                        else:
                            print(f"  {key}: {value}")
                
                return soil_data
            else:
                print(f"❌ Failed to get soil data: {response.status_code}")
                print(f"📄 Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching soil data: {e}")
            return None
    
    def test_multiple_locations(self):
        """Test multiple Kenya locations"""
        locations = [
            (-1.2921, 36.8219, "Nairobi"),
            (-0.0236, 37.9062, "Meru"),
            (-4.0435, 39.6682, "Mombasa"),
            (0.5167, 35.2831, "Eldoret")
        ]
        
        print(f"\n🗺️ Testing multiple locations in Kenya...")
        
        for lat, lon, city in locations:
            data = self.test_soil_properties(lat, lon)
            if data:
                print(f"✅ {city}: Data available")
            else:
                print(f"❌ {city}: No data available")

def main():
    """Main test function"""
    tester = ISDATest()
    
    print("🚀 iSDA API Test Script")
    print("=" * 50)
    
    # Get credentials from user
    print("Please enter your iSDA API credentials:")
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    if not email or not password:
        print("❌ Email and password are required!")
        return
    
    # Authenticate
    if tester.authenticate(email, password):
        # Test single location
        soil_data = tester.test_soil_properties()
        
        # Test multiple locations
        tester.test_multiple_locations()
        
        print(f"\n🎉 iSDA API test completed!")
        print(f"📅 Test completed at: {datetime.now().isoformat()}")
    else:
        print(f"\n❌ Authentication failed. Please check your credentials.")

if __name__ == "__main__":
    main()
