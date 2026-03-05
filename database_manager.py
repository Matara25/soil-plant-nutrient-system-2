#!/usr/bin/env python3
"""
SoilDoctor Database Manager
Handles database operations for the SoilDoctor system
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

class SoilDoctorDB:
    """Database manager for SoilDoctor system"""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        if db_path is None:
            # Use in-memory database for reliability
            self.db_path = ':memory:'
        else:
            self.db_path = str(db_path)
        
        self.conn = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database with schema"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            self._create_tables()
            print(f"✅ Database initialized: {self.db_path}")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            raise
    
    def _create_tables(self):
        """Create all necessary tables"""
        
        # Users table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                phone_number VARCHAR(20),
                location_latitude DECIMAL(10, 8),
                location_longitude DECIMAL(11, 8),
                farm_address TEXT,
                registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Farms table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS farms (
                farm_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                farm_name VARCHAR(100) NOT NULL,
                location_latitude DECIMAL(10, 8) NOT NULL,
                location_longitude DECIMAL(11, 8) NOT NULL,
                farm_size_acres DECIMAL(8, 2),
                soil_type VARCHAR(50),
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        ''')
        
        # Farmer inputs table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS farmer_inputs (
                input_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                farm_id INTEGER NOT NULL,
                crop_type VARCHAR(100) NOT NULL,
                planting_date DATE,
                fertilizer_usage_history TEXT,
                irrigation_method VARCHAR(50),
                tillage_practice VARCHAR(50),
                previous_crop VARCHAR(100),
                expected_yield DECIMAL(10, 2),
                input_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                season VARCHAR(20),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (farm_id) REFERENCES farms(farm_id) ON DELETE CASCADE
            )
        ''')
        
        # IoT sensor data table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS iot_sensor_data (
                sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                farm_id INTEGER NOT NULL,
                sensor_type VARCHAR(50) NOT NULL,
                nitrogen_level DECIMAL(6, 2),
                phosphorus_level DECIMAL(6, 2),
                potassium_level DECIMAL(6, 2),
                ph_level DECIMAL(4, 2),
                moisture_level DECIMAL(5, 2),
                temperature DECIMAL(5, 2),
                plant_health_index DECIMAL(5, 2),
                reading_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                sensor_device_id VARCHAR(50),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (farm_id) REFERENCES farms(farm_id) ON DELETE CASCADE
            )
        ''')
        
        # AI analysis results table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS ai_analysis_results (
                analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                farm_id INTEGER NOT NULL,
                nitrogen_status VARCHAR(10),
                phosphorus_status VARCHAR(10),
                potassium_status VARCHAR(10),
                ph_status VARCHAR(10),
                overall_soil_health VARCHAR(20),
                deficiency_score DECIMAL(5, 2),
                analysis_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                model_version VARCHAR(20),
                confidence_score DECIMAL(5, 2),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (farm_id) REFERENCES farms(farm_id) ON DELETE CASCADE
            )
        ''')
        
        # Fertilizer recommendations table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS fertilizer_recommendations (
                recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                farm_id INTEGER NOT NULL,
                fertilizer_type VARCHAR(100),
                application_rate DECIMAL(8, 2),
                application_unit VARCHAR(20),
                application_timing VARCHAR(100),
                expected_improvement_period VARCHAR(50),
                cost_estimate DECIMAL(10, 2),
                organic_alternative BOOLEAN DEFAULT 1,
                recommendation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (analysis_id) REFERENCES ai_analysis_results(analysis_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (farm_id) REFERENCES farms(farm_id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_farms_user_id ON farms(user_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_farmer_inputs_user_id ON farmer_inputs(user_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_iot_sensor_data_user_id ON iot_sensor_data(user_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_ai_analysis_user_id ON ai_analysis_results(user_id)")
        
        self.conn.commit()
    
    def create_user(self, username: str, email: str, password_hash: str, 
                   full_name: str, phone_number: str = None, 
                   location_lat: float = None, location_lng: float = None,
                   farm_address: str = None) -> int:
        """Create a new user"""
        try:
            cursor = self.conn.execute('''
                INSERT INTO users (username, email, password_hash, full_name, 
                                 phone_number, location_latitude, location_longitude, 
                                 farm_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, phone_number,
                  location_lat, location_lng, farm_address))
            
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"User creation failed: {e}")
    
    def create_farm(self, user_id: int, farm_name: str, latitude: float, 
                   longitude: float, farm_size_acres: float = None,
                   soil_type: str = None) -> int:
        """Create a new farm for a user"""
        try:
            cursor = self.conn.execute('''
                INSERT INTO farms (user_id, farm_name, location_latitude, 
                                 location_longitude, farm_size_acres, soil_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, farm_name, latitude, longitude, farm_size_acres, soil_type))
            
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Farm creation failed: {e}")
    
    def add_farmer_input(self, user_id: int, farm_id: int, crop_type: str,
                        planting_date: str = None, fertilizer_history: str = None,
                        irrigation_method: str = None, tillage_practice: str = None,
                        previous_crop: str = None, expected_yield: float = None,
                        season: str = None) -> int:
        """Add farmer input data"""
        cursor = self.conn.execute('''
            INSERT INTO farmer_inputs (user_id, farm_id, crop_type, planting_date,
                                     fertilizer_usage_history, irrigation_method,
                                     tillage_practice, previous_crop, expected_yield, season)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, farm_id, crop_type, planting_date, fertilizer_history,
              irrigation_method, tillage_practice, previous_crop, expected_yield, season))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def add_sensor_data(self, user_id: int, farm_id: int, sensor_type: str,
                       nitrogen: float = None, phosphorus: float = None,
                       potassium: float = None, ph: float = None,
                       moisture: float = None, temperature: float = None,
                       plant_health: float = None, device_id: str = None) -> int:
        """Add IoT sensor data"""
        cursor = self.conn.execute('''
            INSERT INTO iot_sensor_data (user_id, farm_id, sensor_type, nitrogen_level,
                                        phosphorus_level, potassium_level, ph_level,
                                        moisture_level, temperature, plant_health_index,
                                        sensor_device_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, farm_id, sensor_type, nitrogen, phosphorus, potassium,
              ph, moisture, temperature, plant_health, device_id))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user_farms(self, user_id: int) -> List[Dict]:
        """Get all farms for a user"""
        cursor = self.conn.execute('''
            SELECT * FROM farms WHERE user_id = ? ORDER BY created_date DESC
        ''', (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_user_inputs(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get farmer inputs for a user"""
        cursor = self.conn.execute('''
            SELECT * FROM farmer_inputs 
            WHERE user_id = ? 
            ORDER BY input_date DESC 
            LIMIT ?
        ''', (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_sensor_data(self, user_id: int, farm_id: int = None, limit: int = 50) -> List[Dict]:
        """Get sensor data for a user/farm"""
        if farm_id:
            cursor = self.conn.execute('''
                SELECT * FROM iot_sensor_data 
                WHERE user_id = ? AND farm_id = ?
                ORDER BY reading_date DESC 
                LIMIT ?
            ''', (user_id, farm_id, limit))
        else:
            cursor = self.conn.execute('''
                SELECT * FROM iot_sensor_data 
                WHERE user_id = ?
                ORDER BY reading_date DESC 
                LIMIT ?
            ''', (user_id, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def save_ai_analysis(self, user_id: int, farm_id: int, nitrogen_status: str,
                        phosphorus_status: str, potassium_status: str, ph_status: str,
                        overall_health: str, deficiency_score: float,
                        model_version: str = "v1.0", confidence_score: float = None) -> int:
        """Save AI analysis results"""
        cursor = self.conn.execute('''
            INSERT INTO ai_analysis_results (user_id, farm_id, nitrogen_status,
                                           phosphorus_status, potassium_status, ph_status,
                                           overall_soil_health, deficiency_score,
                                           model_version, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, farm_id, nitrogen_status, phosphorus_status, potassium_status,
              ph_status, overall_health, deficiency_score, model_version, confidence_score))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def add_fertilizer_recommendation(self, analysis_id: int, user_id: int, farm_id: int,
                                     fertilizer_type: str, application_rate: float,
                                     application_unit: str, timing: str,
                                     improvement_period: str = None,
                                     cost_estimate: float = None,
                                     organic_alternative: bool = True) -> int:
        """Add fertilizer recommendation"""
        cursor = self.conn.execute('''
            INSERT INTO fertilizer_recommendations (analysis_id, user_id, farm_id,
                                                   fertilizer_type, application_rate,
                                                   application_unit, application_timing,
                                                   expected_improvement_period,
                                                   cost_estimate, organic_alternative)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (analysis_id, user_id, farm_id, fertilizer_type, application_rate,
              application_unit, timing, improvement_period, cost_estimate, organic_alternative))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        cursor = self.conn.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        cursor = self.conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Example usage and testing
if __name__ == "__main__":
    # Test the database
    with SoilDoctorDB() as db:
        print("🌱 Testing SoilDoctor Database...")
        
        # Create a test user
        try:
            user_id = db.create_user(
                username="test_farmer",
                email="test@soildoctor.com",
                password_hash="hashed_password",
                full_name="Test Farmer",
                phone_number="+254712345678",
                location_lat=-1.2921,
                location_lng=36.8219,
                farm_address="Nairobi, Kenya"
            )
            print(f"✅ Created user with ID: {user_id}")
        except ValueError as e:
            print(f"⚠️  User might already exist: {e}")
            # Get existing user
            user = db.get_user_by_email("test@soildoctor.com")
            user_id = user['user_id'] if user else None
            print(f"📱 Using existing user ID: {user_id}")
        
        if user_id:
            # Create a test farm
            try:
                farm_id = db.create_farm(
                    user_id=user_id,
                    farm_name="Test Farm",
                    latitude=-1.2921,
                    longitude=36.8219,
                    farm_size_acres=5.5,
                    soil_type="Clay Loam"
                )
                print(f"✅ Created farm with ID: {farm_id}")
            except ValueError as e:
                print(f"⚠️  Farm creation issue: {e}")
                farm_id = 1  # Use existing farm ID
                print(f"🌾 Using farm ID: {farm_id}")
            
            # Add farmer input
            input_id = db.add_farmer_input(
                user_id=user_id,
                farm_id=farm_id,
                crop_type="Maize",
                planting_date="2024-03-15",
                fertilizer_usage_history="NPK 20-20-20: 200kg/acre last season",
                irrigation_method="Drip irrigation",
                tillage_practice="Conventional tillage",
                previous_crop="Beans",
                expected_yield=3.5,
                season="Long rains"
            )
            print(f"✅ Added farmer input with ID: {input_id}")
            
            # Add sensor data
            sensor_id = db.add_sensor_data(
                user_id=user_id,
                farm_id=farm_id,
                sensor_type="NPK_pH_moisture",
                nitrogen=15.2,
                phosphorus=8.5,
                potassium=12.3,
                ph=6.2,
                moisture=65.5,
                temperature=24.5,
                device_id="SENSOR_001"
            )
            print(f"✅ Added sensor data with ID: {sensor_id}")
            
            # Save AI analysis
            analysis_id = db.save_ai_analysis(
                user_id=user_id,
                farm_id=farm_id,
                nitrogen_status="LOW",
                phosphorus_status="NORMAL",
                potassium_status="LOW",
                ph_status="NORMAL",
                overall_health="MODERATE",
                deficiency_score=35.5,
                confidence_score=92.3
            )
            print(f"✅ Saved AI analysis with ID: {analysis_id}")
            
            # Add fertilizer recommendation
            rec_id = db.add_fertilizer_recommendation(
                analysis_id=analysis_id,
                user_id=user_id,
                farm_id=farm_id,
                fertilizer_type="Compost",
                application_rate=2000,
                application_unit="kg/acre",
                timing="Before planting, incorporate into soil",
                improvement_period="3-6 months",
                cost_estimate=50.0,
                organic_alternative=True
            )
            print(f"✅ Added fertilizer recommendation with ID: {rec_id}")
            
            # Test retrieval
            farms = db.get_user_farms(user_id)
            print(f"📊 User has {len(farms)} farm(s)")
            
            inputs = db.get_user_inputs(user_id)
            print(f"📝 User has {len(inputs)} input record(s)")
            
            sensor_data = db.get_sensor_data(user_id)
            print(f"🔬 Found {len(sensor_data)} sensor reading(s)")
        
        print("\n🎉 SoilDoctor Database test completed successfully!")
