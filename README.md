# SoilDoctor User Database

A comprehensive backend database system for the SoilDoctor agricultural platform, designed to store and manage user inputs, soil data, IoT sensor readings, and AI analysis results.

# Project Overview

The SoilDoctor database supports intelligent soil analysis and sustainable fertilizer recommendations for smallholder farmers. It integrates data from multiple sources:

- **Farmer Inputs**: Manual data entry for crop types, fertilizer usage, irrigation methods
- **IoT Sensors**: Real-time soil measurements (NPK, pH, moisture, temperature)
- **Geospatial APIs**: External soil data from SoilGrids, iSDAsoil, SoilHive
- **AI Analysis**: Machine learning results for nutrient deficiency detection
- **Recommendations**: Personalized organic fertilizer suggestions

##  Database Schema

### Core Tables

1. **users** - Farmer authentication and profile management
2. **farms** - Farm-specific information and location data
3. **farmer_inputs** - Manual data entry from farmers
4. **iot_sensor_data** - Real-time sensor measurements
5. **soil_grid_data** - Geospatial soil API responses
6. **ai_analysis_results** - ML model analysis outputs
7. **fertilizer_recommendations** - Personalized recommendations
8. **nutrient_alerts** - Toxicity and deficiency warnings
9. **soil_health_history** - Long-term monitoring data
10. **user_sessions** - Authentication tracking

# Quick Start

# 1. Install Dependencies
```bash
pip install -r requirements.txt
```

# 2. Run the Flask API Server
```bash
python app.py
```
The API will be available at `http://localhost:5000`

# 3. Test the Database
```bash
python database_manager.py
```

# API Endpoints

# Users
- `POST /api/users` - Create new user
- `GET /api/users/{id}` - Get user details

# Farms
- `POST /api/farms` - Create new farm
- `GET /api/users/{user_id}/farms` - Get user's farms

# Data Management
- `POST /api/farmer-inputs` - Add farmer input data
- `POST /api/sensor-data` - Add IoT sensor readings
- `GET /api/sensor-data/{user_id}` - Get sensor data

# Analysis
- `POST /api/analysis` - Save AI analysis results
- `POST /api/recommendations` - Add fertilizer recommendations

# Database Manager

The `database_manager.py` file provides a Python class `SoilDoctorDB` with methods for:

- User management (`create_user`, `get_user_by_email`)
- Farm management (`create_farm`, `get_user_farms`)
- Data entry (`add_farmer_input`, `add_sensor_data`)
- AI analysis (`save_ai_analysis`, `add_fertilizer_recommendation`)
- Data retrieval (`get_user_inputs`, `get_sensor_data`)

# 📝 Example Usage

```python
from database_manager import SoilDoctorDB

# Initialize database
with SoilDoctorDB() as db:
    # Create user
    user_id = db.create_user(
        username="john_farmer",
        email="john@soildoctor.com",
        password_hash="hashed_password",
        full_name="John Farmer"
    )
    
    # Create farm
    farm_id = db.create_farm(
        user_id=user_id,
        farm_name="Green Valley Farm",
        latitude=-1.2921,
        longitude=36.8219
    )
    
    # Add sensor data
    sensor_id = db.add_sensor_data(
        user_id=user_id,
        farm_id=farm_id,
        sensor_type="NPK_pH_moisture",
        nitrogen=15.2,
        phosphorus=8.5,
        potassium=12.3,
        ph=6.2
    )
```

# 🏗️ System Architecture Integration

The database supports the SoilDoctor system architecture:

1. **Input Layer**: Stores data from farmer dashboards and IoT sensors
2. **Backend & Intelligence**: Manages data validation, processing, and AI analysis
3. **Cloud & External Services**: Integrates with soil grid APIs and cloud storage

#🔒 Security Features

- Password hashing for user authentication
- Session management for API access
- Data validation and sanitization
- Foreign key constraints for data integrity

# 📈 Performance Optimizations

- Indexed columns for fast queries
- Efficient data retrieval methods
- Connection pooling support
- Batch operations for bulk data

# 🌍 Geographic Support

- Latitude/longitude storage for precise farm locations
- Support for multiple coordinate systems
- Location-based data queries
- Integration with global soil databases

# 📱 Mobile & Web Ready

The database is designed to support both:
- Web dashboards for detailed analysis
- Mobile applications for field data entry
- API-first architecture for flexible integration

# 🔬 Data Types Supported

# Soil Measurements
- Nitrogen (N) levels
- Phosphorus (P) levels  
- Potassium (K) levels
- pH levels
- Soil moisture
- Temperature
- Organic matter content

# Farm Management
- Crop types and rotation
- Fertilizer usage history
- Irrigation methods
- Tillage practices
- Yield expectations

# AI Analysis
- Nutrient status classification (LOW/NORMAL/HIGH)
- Deficiency scoring
- Confidence ratings
- Model versioning

# Deployment

The database can be deployed in various environments:
- **Development**: SQLite (included)
- **Production**: PostgreSQL/MySQL (migrate schema)
- **Cloud**: AWS RDS, Google Cloud SQL, Azure Database

# Support

For technical support or questions about the database:
- Check the API documentation
- Review the schema in `database_schema.sql`
- Test with the provided examples

---

**SoilDoctor Database** - Empowering sustainable agriculture through intelligent soil management 
