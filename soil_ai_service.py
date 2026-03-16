"""
Soil AI Service (SAS)
Service layer for Soil Health Risk Prediction AI integration with SoilDoctor system
"""

import pandas as pd
import numpy as np
from soil_health_risk_prediction import SoilHealthRiskPrediction
import requests
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SoilAIService:
    """Service class for Soil AI integration with external APIs and database operations"""
    
    def __init__(self, model_type='random_forest'):
        """
        Initialize Soil AI Service
        
        Args:
            model_type (str): Type of ML model to use
        """
        self.shrp_model = SoilHealthRiskPrediction(model_type=model_type)
        self.isda_api_url = "https://api.isda-africa.com/isdasoil/v2"
        self.api_token = None
        self.model_trained = False
        
    def authenticate_isda_api(self, email, password):
        """
        Authenticate with iSDA API
        
        Args:
            email (str): iSDA API email
            password (str): iSDA API password
            
        Returns:
            bool: Authentication success status
        """
        try:
            auth_url = f"{self.isda_api_url}/login"
            headers = {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = f"username={email}&password={password}"
            
            response = requests.post(auth_url, headers=headers, data=data)
            
            if response.status_code == 200:
                auth_data = response.json()
                self.api_token = auth_data.get('token')
                logger.info("Successfully authenticated with iSDA API")
                return True
            else:
                logger.error(f"Authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False
    
    def fetch_soil_data_from_isda(self, latitude, longitude, radius=100):
        """
        Fetch soil data from iSDA API for specific location
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            radius (int): Search radius in meters
            
        Returns:
            dict: Soil data from iSDA API
        """
        if not self.api_token:
            logger.error("Not authenticated with iSDA API")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "accept": "application/json"
            }
            
            # Query soil data for the location
            soil_url = f"{self.isda_api_url}/soil-properties"
            params = {
                "lat": latitude,
                "lon": longitude,
                "radius": radius
            }
            
            response = requests.get(soil_url, headers=headers, params=params)
            
            if response.status_code == 200:
                soil_data = response.json()
                logger.info(f"Successfully fetched soil data for {latitude}, {longitude}")
                return soil_data
            else:
                logger.error(f"Failed to fetch soil data: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching soil data: {e}")
            return None
    
    def load_training_data(self, file_path=None, use_isda_data=False, locations=None):
        """
        Load training data from CSV file or iSDA API
        
        Args:
            file_path (str): Path to local CSV file
            use_isda_data (bool): Whether to use iSDA API data
            locations (list): List of (lat, lon) tuples for iSDA data
            
        Returns:
            pd.DataFrame: Training dataset
        """
        if file_path:
            # Load from local file
            data = self.shrp_model.load_and_preprocess_data(file_path)
            if data is not None:
                logger.info(f"Loaded training data from {file_path}")
                return data
        
        elif use_isda_data and locations:
            # Fetch data from iSDA API for multiple locations
            all_data = []
            
            for lat, lon in locations:
                soil_data = self.fetch_soil_data_from_isda(lat, lon)
                if soil_data:
                    # Convert iSDA data to our format
                    processed_data = self._convert_isda_to_training_format(soil_data, lat, lon)
                    all_data.append(processed_data)
            
            if all_data:
                combined_data = pd.concat(all_data, ignore_index=True)
                logger.info(f"Combined {len(all_data)} location datasets")
                return combined_data
        
        else:
            logger.error("No data source provided")
            return None
    
    def _convert_isda_to_training_format(self, isda_data, latitude, longitude):
        """
        Convert iSDA API data to training format
        
        Args:
            isda_data (dict): Data from iSDA API
            latitude (float): Location latitude
            longitude (float): Location longitude
            
        Returns:
            pd.DataFrame: Formatted training data
        """
        # Extract relevant soil properties from iSDA data
        # This is a simplified conversion - adjust based on actual iSDA API response structure
        
        records = []
        
        if 'properties' in isda_data:
            props = isda_data['properties']
            
            record = {
                'latitude': latitude,
                'longitude': longitude,
                'nitrogen': props.get('nitrogen', np.random.normal(1.5, 0.5)),
                'phosphorus': props.get('phosphorus', np.random.normal(25, 10)),
                'potassium': props.get('potassium', np.random.normal(200, 50)),
                'organic_matter': props.get('organic_matter', np.random.normal(2.5, 1.0)),
                'ph': props.get('ph', np.random.normal(6.5, 1.0)),
                'soil_type': props.get('soil_type', 'loam'),
                'erosion_level': props.get('erosion_level', 'moderate'),
                'fertilizer_usage': props.get('fertilizer_usage', 'moderate'),
                'crop_rotation': props.get('crop_rotation', 'yes'),
                'organic_amendments': props.get('organic_amendments', 'compost')
            }
            
            records.append(record)
        
        return pd.DataFrame(records)
    
    def train_ai_models(self, training_data):
        """
        Train AI models with provided data
        
        Args:
            training_data (pd.DataFrame): Training dataset
            
        Returns:
            bool: Training success status
        """
        try:
            if training_data is None or len(training_data) == 0:
                logger.error("No training data provided")
                return False
            
            # Train the models
            self.shrp_model.train_models(training_data)
            self.model_trained = True
            
            logger.info("AI models trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return False
    
    def analyze_soil_health(self, soil_data, location=None):
        """
        Comprehensive soil health analysis
        
        Args:
            soil_data (dict or pd.DataFrame): Soil data for analysis
            location (tuple): (latitude, longitude) for location-based analysis
            
        Returns:
            dict: Comprehensive soil health analysis
        """
        if not self.model_trained:
            logger.error("Models not trained yet")
            return None
        
        try:
            # Convert input to DataFrame if needed
            if isinstance(soil_data, dict):
                soil_df = pd.DataFrame([soil_data])
            else:
                soil_df = soil_data.copy()
            
            # Add location data if provided
            if location:
                soil_df['latitude'] = location[0]
                soil_df['longitude'] = location[1]
            
            # Run all predictions
            degradation_risks = self.shrp_model.predict_degradation_risk(soil_df)
            nutrient_toxicity = self.shrp_model.predict_nutrient_toxicity(soil_df)
            fertility_trends = self.shrp_model.predict_fertility_trend(soil_df)
            
            # Combine results
            analysis_results = []
            
            for i in range(len(soil_df)):
                result = {
                    'location': {
                        'latitude': soil_df.iloc[i].get('latitude'),
                        'longitude': soil_df.iloc[i].get('longitude')
                    },
                    'degradation_risk': degradation_risks[i],
                    'nutrient_toxicity': nutrient_toxicity[i],
                    'fertility_trend': fertility_trends[i],
                    'overall_health_score': self._calculate_overall_health_score(
                        degradation_risks[i], 
                        nutrient_toxicity[i], 
                        fertility_trends[i]
                    ),
                    'recommendations': self._generate_comprehensive_recommendations(
                        degradation_risks[i], 
                        nutrient_toxicity[i], 
                        fertility_trends[i]
                    ),
                    'analysis_timestamp': datetime.now().isoformat()
                }
                
                analysis_results.append(result)
            
            return analysis_results[0] if len(analysis_results) == 1 else analysis_results
            
        except Exception as e:
            logger.error(f"Soil health analysis failed: {e}")
            return None
    
    def _calculate_overall_health_score(self, degradation_risk, toxicity, fertility):
        """
        Calculate overall soil health score (0-100)
        
        Args:
            degradation_risk (dict): Degradation risk assessment
            toxicity (dict): Nutrient toxicity assessment
            fertility (dict): Fertility trend assessment
            
        Returns:
            float: Overall health score
        """
        score = 50  # Base score
        
        # Adjust based on degradation risk
        risk_level = degradation_risk['risk_level']
        if risk_level == 'LOW':
            score += 20
        elif risk_level == 'MEDIUM':
            score += 10
        elif risk_level == 'HIGH':
            score -= 10
        elif risk_level == 'CRITICAL':
            score -= 20
        
        # Adjust based on toxicity
        toxicity_level = toxicity['toxicity_level']
        if toxicity_level == 'NONE':
            score += 15
        elif toxicity_level == 'LOW':
            score += 5
        elif toxicity_level == 'MODERATE':
            score -= 5
        elif toxicity_level == 'HIGH':
            score -= 15
        
        # Adjust based on fertility index
        fertility_index = fertility['fertility_index']
        score += (fertility_index - 50) * 0.3
        
        # Ensure score is within 0-100 range
        return max(0, min(100, score))
    
    def _generate_comprehensive_recommendations(self, degradation_risk, toxicity, fertility):
        """
        Generate comprehensive recommendations based on all analyses
        
        Args:
            degradation_risk (dict): Degradation risk assessment
            toxicity (dict): Nutrient toxicity assessment
            fertility (dict): Fertility trend assessment
            
        Returns:
            list: Comprehensive recommendations
        """
        recommendations = []
        
        # Recommendations based on degradation risk
        risk_level = degradation_risk['risk_level']
        if risk_level in ['HIGH', 'CRITICAL']:
            recommendations.extend([
                "Implement immediate soil conservation measures",
                "Add organic matter (compost, manure, green manures)",
                "Establish cover crops to prevent erosion",
                "Reduce tillage intensity"
            ])
        elif risk_level == 'MEDIUM':
            recommendations.extend([
                "Monitor soil health regularly",
                "Consider crop rotation improvements",
                "Add organic amendments"
            ])
        
        # Recommendations based on toxicity
        toxicity_level = toxicity['toxicity_level']
        if toxicity_level in ['MODERATE', 'HIGH']:
            recommendations.extend([
                "Reduce chemical fertilizer applications",
                "Conduct detailed nutrient analysis",
                "Implement nutrient management plan",
                "Consider soil flushing if toxicity is severe"
            ])
        
        # Recommendations based on fertility trend
        fertility_trend = fertility['trend']
        if fertility_trend == 'Declining':
            recommendations.extend([
                "Increase organic matter additions",
                "Implement sustainable farming practices",
                "Add cover crops and green manures"
            ])
        elif fertility_trend == 'Critical':
            recommendations.extend([
                "Immediate soil rehabilitation required",
                "Consult agricultural extension services",
                "Consider resting the field temporarily"
            ])
        
        # General recommendations
        recommendations.extend([
            "Regular soil testing (at least annually)",
            "Maintain detailed farm records",
            "Practice integrated nutrient management"
        ])
        
        return list(set(recommendations))  # Remove duplicates
    
    def get_soil_health_report(self, latitude, longitude, soil_data=None):
        """
        Get comprehensive soil health report for a specific location
        
        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            soil_data (dict): Optional local soil measurements
            
        Returns:
            dict: Comprehensive soil health report
        """
        # If no soil data provided, try to fetch from iSDA
        if soil_data is None:
            isda_data = self.fetch_soil_data_from_isda(latitude, longitude)
            if isda_data:
                soil_data = self._convert_isda_to_training_format(isda_data, latitude, longitude).iloc[0].to_dict()
            else:
                logger.error("No soil data available for this location")
                return None
        
        # Analyze soil health
        analysis = self.analyze_soil_health(soil_data, (latitude, longitude))
        
        if analysis:
            # Add additional context
            analysis['location_info'] = {
                'coordinates': {'lat': latitude, 'lon': longitude},
                'data_source': 'iSDA API' if soil_data.get('from_isda') else 'Local measurements'
            }
            
            # Add action plan
            analysis['action_plan'] = self._create_action_plan(analysis)
        
        return analysis
    
    def _create_action_plan(self, analysis):
        """
        Create actionable plan based on soil health analysis
        
        Args:
            analysis (dict): Soil health analysis results
            
        Returns:
            dict: Action plan with priorities and timeline
        """
        health_score = analysis['overall_health_score']
        degradation_risk = analysis['degradation_risk']['risk_level']
        
        plan = {
            'immediate_actions': [],
            'short_term_actions': [],
            'long_term_actions': [],
            'monitoring_requirements': []
        }
        
        if health_score < 40 or degradation_risk in ['HIGH', 'CRITICAL']:
            plan['immediate_actions'].extend([
                "Stop chemical fertilizer applications immediately",
                "Add large amounts of organic matter",
                "Implement emergency erosion control"
            ])
        
        if health_score < 60:
            plan['short_term_actions'].extend([
                "Develop nutrient management plan",
                "Plant cover crops",
                "Reduce tillage intensity"
            ])
        
        plan['long_term_actions'].extend([
            "Establish regular soil testing schedule",
            "Implement crop rotation system",
            "Build soil organic matter over time"
        ])
        
        plan['monitoring_requirements'].extend([
            "Monthly soil moisture checks",
            "Quarterly nutrient testing",
            "Annual comprehensive soil analysis"
        ])
        
        return plan

# Example usage and testing
def test_soil_ai_service():
    """Test the Soil AI Service"""
    print("=== Soil AI Service Test ===")
    
    # Initialize service
    soil_service = SoilAIService(model_type='random_forest')
    
    # Create sample training data
    training_data = pd.DataFrame({
        'nitrogen': np.random.normal(1.5, 0.5, 100),
        'phosphorus': np.random.normal(25, 10, 100),
        'potassium': np.random.normal(200, 50, 100),
        'organic_matter': np.random.normal(2.5, 1.0, 100),
        'ph': np.random.normal(6.5, 1.0, 100),
        'soil_type': np.random.choice(['loam', 'clay', 'sandy'], 100),
        'erosion_level': np.random.choice(['low', 'moderate', 'high'], 100),
        'fertilizer_usage': np.random.choice(['low', 'moderate', 'high'], 100),
        'crop_rotation': np.random.choice(['yes', 'no'], 100),
        'organic_amendments': np.random.choice(['compost', 'manure', 'none'], 100)
    })
    
    print("Sample training data created")
    
    # Train models
    if soil_service.train_ai_models(training_data):
        print("Models trained successfully")
        
        # Test analysis
        sample_soil = {
            'nitrogen': 1.2,
            'phosphorus': 28,
            'potassium': 180,
            'organic_matter': 3.1,
            'ph': 6.8,
            'soil_type': 'loam',
            'erosion_level': 'moderate',
            'fertilizer_usage': 'moderate',
            'crop_rotation': 'yes',
            'organic_amendments': 'compost'
        }
        
        # Analyze soil health
        analysis = soil_service.analyze_soil_health(sample_soil, (-1.2921, 36.8219))
        
        if analysis:
            print("\n=== Soil Health Analysis Results ===")
            print(f"Overall Health Score: {analysis['overall_health_score']:.1f}/100")
            print(f"Degradation Risk: {analysis['degradation_risk']['risk_level']}")
            print(f"Nutrient Toxicity: {analysis['nutrient_toxicity']['toxicity_level']}")
            print(f"Fertility Trend: {analysis['fertility_trend']['trend']}")
            
            print("\nRecommendations:")
            for rec in analysis['recommendations'][:5]:  # Show first 5
                print(f"- {rec}")
        else:
            print("Analysis failed")
    else:
        print("Model training failed")

if __name__ == "__main__":
    test_soil_ai_service()
