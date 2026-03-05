-- SoilDoctor User Database Schema


-- Users table for farmer authentication and profile management
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
);

-- Farms table to store farm-specific information
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
);

-- Farmer inputs table for manual data entry
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
);

-- IoT sensor data table for real-time measurements
CREATE TABLE IF NOT EXISTS iot_sensor_data (
    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_id INTEGER NOT NULL,
    sensor_type VARCHAR(50) NOT NULL, -- pH, NPK, moisture, plant_health
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
);

-- Soil Grid API responses table for geospatial data
CREATE TABLE IF NOT EXISTS soil_grid_data (
    grid_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_id INTEGER NOT NULL,
    location_latitude DECIMAL(10, 8) NOT NULL,
    location_longitude DECIMAL(11, 8) NOT NULL,
    api_nitrogen DECIMAL(6, 2),
    api_phosphorus DECIMAL(6, 2),
    api_potassium DECIMAL(6, 2),
    api_ph DECIMAL(4, 2),
    api_organic_matter DECIMAL(5, 2),
    api_soil_texture VARCHAR(50),
    api_response_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    api_source VARCHAR(50), -- iSDAsoil, SoilGrids, SoilHive
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (farm_id) REFERENCES farms(farm_id) ON DELETE CASCADE
);

-- AI analysis results table
CREATE TABLE IF NOT EXISTS ai_analysis_results (
    analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_id INTEGER NOT NULL,
    nitrogen_status VARCHAR(10), -- LOW, NORMAL, HIGH
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
);

-- Fertilizer recommendations table
CREATE TABLE IF NOT EXISTS fertilizer_recommendations (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    farm_id INTEGER NOT NULL,
    fertilizer_type VARCHAR(100), -- compost, manure, green_manure, etc.
    application_rate DECIMAL(8, 2),
    application_unit VARCHAR(20), -- kg/acre, tons/hectare
    application_timing VARCHAR(100),
    expected_improvement_period VARCHAR(50),
    cost_estimate DECIMAL(10, 2),
    organic_alternative BOOLEAN DEFAULT 1,
    recommendation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (analysis_id) REFERENCES ai_analysis_results(analysis_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (farm_id) REFERENCES farms(farm_id) ON DELETE CASCADE
);

-- Nutrient alerts table for toxicity warnings
CREATE TABLE IF NOT EXISTS nutrient_alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_id INTEGER NOT NULL,
    alert_type VARCHAR(50), -- toxicity, deficiency, imbalance
    nutrient_involved VARCHAR(50),
    severity_level VARCHAR(20), -- LOW, MEDIUM, HIGH, CRITICAL
    alert_message TEXT,
    recommended_action TEXT,
    alert_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_resolved BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (farm_id) REFERENCES farms(farm_id) ON DELETE CASCADE
);

-- Historical data tracking for long-term monitoring
CREATE TABLE IF NOT EXISTS soil_health_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_id INTEGER NOT NULL,
    measurement_date DATE,
    soil_organic_matter DECIMAL(5, 2),
    soil_ph DECIMAL(4, 2),
    nitrogen_content DECIMAL(6, 2),
    phosphorus_content DECIMAL(6, 2),
    potassium_content DECIMAL(6, 2),
    crop_yield DECIMAL(10, 2),
    fertilizer_used DECIMAL(10, 2),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (farm_id) REFERENCES farms(farm_id) ON DELETE CASCADE
);

-- User sessions for authentication tracking
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    device_info TEXT,
    ip_address VARCHAR(45),
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiry_time DATETIME,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_farms_user_id ON farms(user_id);
CREATE INDEX IF NOT EXISTS idx_farmer_inputs_user_id ON farmer_inputs(user_id);
CREATE INDEX IF NOT EXISTS idx_farmer_inputs_farm_id ON farmer_inputs(farm_id);
CREATE INDEX IF NOT EXISTS idx_iot_sensor_data_user_id ON iot_sensor_data(user_id);
CREATE INDEX IF NOT EXISTS idx_iot_sensor_data_farm_id ON iot_sensor_data(farm_id);
CREATE INDEX IF NOT EXISTS idx_iot_sensor_data_date ON iot_sensor_data(reading_date);
CREATE INDEX IF NOT EXISTS idx_soil_grid_data_user_id ON soil_grid_data(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_analysis_user_id ON ai_analysis_results(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON fertilizer_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_alerts_user_id ON nutrient_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON nutrient_alerts(is_resolved);
CREATE INDEX IF NOT EXISTS idx_soil_history_user_id ON soil_health_history(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);
