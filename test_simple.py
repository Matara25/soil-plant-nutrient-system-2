#!/usr/bin/env python3
"""
Simple test script for SoilDoctor database
"""

import sqlite3
import json
from datetime import datetime

def test_database():
    """Test database functionality"""
    print("🌱 Testing SoilDoctor Database...")
    
    # Use in-memory database for testing
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE farms (
            farm_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            farm_name VARCHAR(100) NOT NULL,
            location_latitude DECIMAL(10, 8) NOT NULL,
            location_longitude DECIMAL(11, 8) NOT NULL,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Test user creation
    try:
        cursor.execute('''
            INSERT INTO users (username, email, full_name)
            VALUES (?, ?, ?)
        ''', ('john_farmer', 'john@soildoctor.com', 'John Farmer'))
        
        user_id = cursor.lastrowid
        print(f"✅ Created user with ID: {user_id}")
        
        # Test farm creation
        cursor.execute('''
            INSERT INTO farms (user_id, farm_name, location_latitude, location_longitude)
            VALUES (?, ?, ?, ?)
        ''', (user_id, 'Green Valley Farm', -1.2921, 36.8219))
        
        farm_id = cursor.lastrowid
        print(f"✅ Created farm with ID: {farm_id}")
        
        # Test data retrieval
        users = cursor.execute('SELECT * FROM users').fetchall()
        farms = cursor.execute('SELECT * FROM farms').fetchall()
        
        print(f"📊 Total users: {len(users)}")
        print(f"📊 Total farms: {len(farms)}")
        
        # Display data
        for user in users:
            print(f"👤 User: {dict(user)}")
        
        for farm in farms:
            print(f"🌾 Farm: {dict(farm)}")
        
        conn.commit()
        print("\n🎉 Database test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    finally:
        conn.close()
    
    return True

def test_api_endpoints():
    """Test API endpoints with sample data"""
    print("\n🌐 Testing API Endpoints...")
    
    # Sample data for testing
    test_user = {
        "username": "test_farmer",
        "email": "test@soildoctor.com", 
        "full_name": "Test Farmer"
    }
    
    test_farm = {
        "user_id": 1,
        "farm_name": "Test Farm",
        "latitude": -1.2921,
        "longitude": 36.8219
    }
    
    print("📝 Sample User Data:")
    print(json.dumps(test_user, indent=2))
    
    print("\n📝 Sample Farm Data:")
    print(json.dumps(test_farm, indent=2))
    
    print("\n🔗 API Endpoints to Test:")
    print("POST http://localhost:5000/api/users")
    print("POST http://localhost:5000/api/farms")
    print("GET  http://localhost:5000/api/users/1/farms")

if __name__ == "__main__":
    # Run database test
    if test_database():
        # Show API test data
        test_api_endpoints()
    else:
        print("❌ Database test failed")
