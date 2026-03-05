#!/usr/bin/env python3
"""
SoilDoctor Database Setup Script
Initializes SQLite database with schema based on system architecture
"""

import sqlite3
import os
from pathlib import Path

def create_database():
    """Create SQLite database and initialize tables"""
    
    # Define database path
    db_path = Path(__file__).parent / "soildoctor.db"
    conn = None
    
    try:
        # Remove existing database if it exists
        if db_path.exists():
            print(f"Removing existing database: {db_path}")
            db_path.unlink()
        
        # Create new database connection with absolute path
        db_absolute_path = db_path.absolute()
        print(f"Creating database at: {db_absolute_path}")
        conn = sqlite3.connect(str(db_absolute_path))
        cursor = conn.cursor()
        
        # Read and execute schema
        schema_path = Path(__file__).parent / "database_schema.sql"
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Execute schema
        cursor.executescript(schema_sql)
        
        # Commit changes
        conn.commit()
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("✅ Database created successfully!")
        print(f"📍 Database location: {db_path.absolute()}")
        print(f"📊 Tables created: {len(tables)}")
        
        for table in tables:
            print(f"   - {table[0]}")
        
        # Create sample data for testing
        create_sample_data(cursor, conn)
        
        print("\n🎉 SoilDoctor database is ready for use!")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def create_sample_data(cursor, conn):
    """Create sample data for testing the database"""
    
    print("\n📝 Creating sample data...")
    
    # Sample user
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, full_name, phone_number, 
                          location_latitude, location_longitude, farm_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "john_farmer", "john@soildoctor.com", "hashed_password_123", 
        "John Farmer", "+254712345678", -1.2921, 36.8219,
        "Nairobi, Kenya"
    ))
    
    user_id = cursor.lastrowid
    
    # Sample farm
    cursor.execute("""
        INSERT INTO farms (user_id, farm_name, location_latitude, location_longitude, 
                          farm_size_acres, soil_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id, "Green Valley Farm", -1.2921, 36.8219, 5.5, "Clay Loam"
    ))
    
    farm_id = cursor.lastrowid
    
    # Sample farmer input
    cursor.execute("""
        INSERT INTO farmer_inputs (user_id, farm_id, crop_type, planting_date, 
                                  fertilizer_usage_history, irrigation_method, 
                                  tillage_practice, previous_crop, expected_yield, season)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, farm_id, "Maize", "2024-03-15", 
        "NPK 20-20-20: 200kg/acre last season", "Drip irrigation", 
        "Conventional tillage", "Beans", 3.5, "Long rains"
    ))
    
    # Sample IoT sensor data
    cursor.execute("""
        INSERT INTO iot_sensor_data (user_id, farm_id, sensor_type, nitrogen_level, 
                                    phosphorus_level, potassium_level, ph_level, 
                                    moisture_level, temperature, sensor_device_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, farm_id, "NPK_pH_moisture", 15.2, 8.5, 12.3, 6.2, 65.5, 24.5, "SENSOR_001"
    ))
    
    # Sample soil grid API data
    cursor.execute("""
        INSERT INTO soil_grid_data (user_id, farm_id, location_latitude, location_longitude,
                                   api_nitrogen, api_phosphorus, api_potassium, api_ph, 
                                   api_organic_matter, api_soil_texture, api_source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, farm_id, -1.2921, 36.8219, 18.5, 10.2, 15.8, 6.5, 2.8, "Clay Loam", "SoilGrids"
    ))
    
    # Sample AI analysis
    cursor.execute("""
        INSERT INTO ai_analysis_results (user_id, farm_id, nitrogen_status, phosphorus_status,
                                        potassium_status, ph_status, overall_soil_health,
                                        deficiency_score, model_version, confidence_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, farm_id, "LOW", "NORMAL", "LOW", "NORMAL", "MODERATE", 35.5, "v1.0", 92.3
    ))
    
    analysis_id = cursor.lastrowid
    
    # Sample fertilizer recommendations
    cursor.execute("""
        INSERT INTO fertilizer_recommendations (analysis_id, user_id, farm_id, fertilizer_type,
                                               application_rate, application_unit, 
                                               application_timing, expected_improvement_period,
                                               cost_estimate, organic_alternative)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        analysis_id, user_id, farm_id, "Compost", 2000, "kg/acre", 
        "Before planting, incorporate into soil", "3-6 months", 50.0, 1
    ))
    
    # Sample nutrient alert
    cursor.execute("""
        INSERT INTO nutrient_alerts (user_id, farm_id, alert_type, nutrient_involved,
                                     severity_level, alert_message, recommended_action)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, farm_id, "deficiency", "Nitrogen", "MEDIUM",
        "Low nitrogen levels detected. Consider organic fertilizers.",
        "Apply compost or well-rotted manure before planting"
    ))
    
    conn.commit()
    print("✅ Sample data created successfully!")

if __name__ == "__main__":
    create_database()
