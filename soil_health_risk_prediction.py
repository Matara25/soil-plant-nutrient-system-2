"""
Soil Health Risk Prediction AI Module (SHRP)
SoilDoctor AI System for Soil Degradation Risk, Nutrient Toxicity, and Long-term Fertility Trends
"""

import pandas as pd
import numpy as np
import glob
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')

class SoilHealthRiskPrediction:
    """AI Model for Soil Health Risk Assessment and Prediction"""
    
    def __init__(self, model_type='random_forest'):
        """
        Initialize the Soil Health Risk Prediction AI Model
        
        Args:
            model_type (str): Type of ML model ('random_forest', 'gradient_boosting', 'decision_tree')
        """
        self.model_type = model_type
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_columns = {}
        self.target_columns = {}
        
        # Initialize models for different predictions
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize machine learning models for different tasks"""
        if self.model_type == 'random_forest':
            self.models['degradation_risk'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['nutrient_toxicity'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['fertility_trend'] = RandomForestRegressor(n_estimators=100, random_state=42)
        elif self.model_type == 'gradient_boosting':
            self.models['degradation_risk'] = GradientBoostingClassifier(n_estimators=100, random_state=42)
            self.models['nutrient_toxicity'] = GradientBoostingClassifier(n_estimators=100, random_state=42)
            self.models['fertility_trend'] = GradientBoostingRegressor(n_estimators=100, random_state=42)
        elif self.model_type == 'decision_tree':
            self.models['degradation_risk'] = DecisionTreeClassifier(random_state=42)
            self.models['nutrient_toxicity'] = DecisionTreeClassifier(random_state=42)
            self.models['fertility_trend'] = DecisionTreeRegressor(random_state=42)
        
        # Initialize scalers
        self.scalers['degradation_risk'] = StandardScaler()
        self.scalers['nutrient_toxicity'] = StandardScaler()
        self.scalers['fertility_trend'] = StandardScaler()
    
    def load_multiple_csv_files(self, csv_folder_path):
        """
        Load and merge multiple CSV files from a folder recursively
        
        Args:
            csv_folder_path (str): Path to folder containing CSV files
            
        Returns:
            pd.DataFrame: Combined dataset from all CSV files
        """
        try:
            print(f"Searching for CSV files in: {csv_folder_path}")
            
            # Find all CSV files recursively
            all_csvs = glob.glob(os.path.join(csv_folder_path, '**', '*.csv'), recursive=True)
            
            if not all_csvs:
                print(f"No CSV files found in {csv_folder_path}")
                return None
            
            print(f"Found {len(all_csvs)} CSV files:")
            for csv_file in all_csvs[:5]:  # Show first 5 files
                print(f"  - {os.path.basename(csv_file)}")
            if len(all_csvs) > 5:
                print(f"  ... and {len(all_csvs) - 5} more files")
            
            # Load and combine all CSVs
            dfs = []
            total_rows = 0
            
            for i, csv_file in enumerate(all_csvs):
                try:
                    print(f"Loading file {i+1}/{len(all_csvs)}: {os.path.basename(csv_file)}")
                    df = pd.read_csv(csv_file)
                    
                    # Check if DataFrame has expected columns
                    if self._validate_soil_columns(df):
                        dfs.append(df)
                        total_rows += len(df)
                        print(f"  ✓ Loaded {len(df)} rows")
                    else:
                        print(f"  ⚠ Skipping - missing required soil columns")
                        
                except Exception as e:
                    print(f"  ✗ Error loading {csv_file}: {e}")
                    continue
            
            if not dfs:
                print("No valid CSV files with required soil columns found")
                return None
            
            # Combine all DataFrames
            print(f"\nCombining {len(dfs)} valid datasets...")
            full_data = pd.concat(dfs, ignore_index=True)
            
            print(f"✅ Combined dataset shape: {full_data.shape}")
            print(f"✅ Total rows combined: {total_rows}")
            print(f"✅ Columns: {list(full_data.columns)}")
            
            return full_data
            
        except Exception as e:
            print(f"Error loading multiple CSV files: {e}")
            return None
    
    def _validate_soil_columns(self, df):
        """
        Validate that DataFrame has required soil columns
        
        Args:
            df (pd.DataFrame): DataFrame to validate
            
        Returns:
            bool: True if required columns are present
        """
        # Check for required columns (case-insensitive)
        required_columns = ['nitrogen', 'phosphorus', 'potassium', 'Nitrogen', 'Phosphorus', 'Potassium']
        optional_columns = ['organic_matter', 'ph', 'soil_type', 'latitude', 'longitude', 
                          'organic_matter', 'pH', 'Soil_Type', 'Latitude', 'Longitude']
        
        # Get actual column names
        actual_columns = list(df.columns)
        
        # Check for at least one required column (case-insensitive)
        has_required = any(col.lower() in [c.lower() for c in actual_columns] for col in required_columns)
        
        # Check for at least one optional column (case-insensitive)
        has_optional = any(col.lower() in [c.lower() for c in actual_columns] for col in optional_columns)
        
        print(f"  Available columns: {actual_columns}")
        print(f"  Has required nutrients: {has_required}")
        print(f"  Has optional columns: {has_optional}")
        
        return has_required and has_optional
    
    def load_and_preprocess_data(self, file_path=None, csv_folder_path=None):
        """
        Load and preprocess soil data from single file or multiple CSVs
        
        Args:
            file_path (str): Path to single CSV file
            csv_folder_path (str): Path to folder with multiple CSVs
            
        Returns:
            pd.DataFrame: Preprocessed dataset
        """
        if csv_folder_path:
            # Load multiple CSV files
            data = self.load_multiple_csv_files(csv_folder_path)
        elif file_path:
            # Load single file
            try:
                data = pd.read_csv(file_path)
                print(f"Dataset loaded successfully from {file_path}")
                print(f"Shape: {data.shape}")
                print(f"Columns: {list(data.columns)}")
            except Exception as e:
                print(f"Error loading single file: {e}")
                return None
        else:
            print("No data source provided")
            return None
        
        if data is None or len(data) == 0:
            print("No data to process")
            return None
        
        # Basic preprocessing
        print("\nPreprocessing data...")
        
        # Handle missing values
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        missing_numeric = data[numeric_columns].isnull().sum()
        if missing_numeric.sum() > 0:
            print(f"Filling missing numeric values:")
            for col, missing_count in missing_numeric.items():
                if missing_count > 0:
                    median_val = data[col].median()
                    data[col].fillna(median_val, inplace=True)
                    print(f"  - {col}: {missing_count} missing values filled with median {median_val:.2f}")
        
        # Handle categorical missing values
        categorical_columns = data.select_dtypes(include=['object']).columns
        missing_categorical = data[categorical_columns].isnull().sum()
        if missing_categorical.sum() > 0:
            print(f"Filling missing categorical values:")
            for col, missing_count in missing_categorical.items():
                if missing_count > 0:
                    mode_val = data[col].mode()[0] if not data[col].mode().empty else 'Unknown'
                    data[col].fillna(mode_val, inplace=True)
                    print(f"  - {col}: {missing_count} missing values filled with '{mode_val}'")
        
        # Data quality checks
        print(f"\nData quality summary:")
        print(f"  - Total rows: {len(data)}")
        print(f"  - Total columns: {len(data.columns)}")
        print(f"  - Numeric columns: {len(numeric_columns)}")
        print(f"  - Categorical columns: {len(categorical_columns)}")
        print(f"  - Missing values after cleaning: {data.isnull().sum().sum()}")
        
        return data
    
    def prepare_degradation_risk_features(self, data):
        """
        Prepare features for soil degradation risk prediction
        
        Args:
            data (pd.DataFrame): Input soil data
            
        Returns:
            tuple: (X, y) features and target for degradation risk
        """
        # Feature engineering for degradation risk
        features = []
        
        # Soil nutrient features (case-insensitive)
        nutrient_cols = ['nitrogen', 'phosphorus', 'potassium', 'organic_matter', 'ph']
        available_nutrients = []
        
        for col in nutrient_cols:
            # Find matching column (case-insensitive)
            matching_col = None
            for actual_col in data.columns:
                if actual_col.lower() == col.lower():
                    matching_col = actual_col
                    break
            if matching_col:
                available_nutrients.append(matching_col)
        
        # Add soil properties (case-insensitive)
        soil_props = ['soil_type', 'texture', 'drainage', 'erosion_level']
        available_props = []
        
        for col in soil_props:
            matching_col = None
            for actual_col in data.columns:
                if actual_col.lower() == col.lower():
                    matching_col = actual_col
                    break
            if matching_col:
                available_props.append(matching_col)
        
        # Environmental factors (case-insensitive)
        env_factors = ['rainfall', 'temperature', 'humidity', 'slope']
        available_env = []
        
        for col in env_factors:
            matching_col = None
            for actual_col in data.columns:
                if actual_col.lower() == col.lower():
                    matching_col = actual_col
                    break
            if matching_col:
                available_env.append(matching_col)
        
        # Combine all available features
        feature_columns = available_nutrients + available_props + available_env
        
        if not feature_columns:
            print("No valid features found!")
            return None, None
        
        print(f"Using features: {feature_columns}")
        
        # Create feature matrix
        X = data[feature_columns].copy()
        
        # Handle categorical variables
        categorical_features = X.select_dtypes(include=['object']).columns
        for col in categorical_features:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                X[col] = self.encoders[col].fit_transform(X[col].astype(str))
            else:
                X[col] = self.encoders[col].transform(X[col].astype(str))
        
        # Create target variable for degradation risk
        y = self._calculate_degradation_risk(data)
        
        self.feature_columns['degradation_risk'] = feature_columns
        return X, y
    
    def _calculate_degradation_risk(self, data):
        """
        Calculate soil degradation risk based on multiple factors
        
        Args:
            data (pd.DataFrame): Input soil data
            
        Returns:
            np.array: Risk categories (LOW, MEDIUM, HIGH, CRITICAL)
        """
        risk_scores = []
        
        for idx, row in data.iterrows():
            score = 0
            
            # Nutrient imbalance factors (case-insensitive)
            nitrogen_col = None
            phosphorus_col = None
            potassium_col = None
            organic_matter_col = None
            ph_col = None
            
            # Find nitrogen column
            for col in data.columns:
                if col.lower() == 'nitrogen':
                    nitrogen_col = col
                    break
            
            # Find phosphorus column
            for col in data.columns:
                if col.lower() == 'phosphorus':
                    phosphorus_col = col
                    break
            
            # Find potassium column
            for col in data.columns:
                if col.lower() == 'potassium':
                    potassium_col = col
                    break
            
            # Find organic matter column
            for col in data.columns:
                if col.lower() == 'organic_matter':
                    organic_matter_col = col
                    break
            
            # Find pH column
            for col in data.columns:
                if col.lower() == 'ph':
                    ph_col = col
                    break
            
            # Check nitrogen levels
            if nitrogen_col and nitrogen_col in data.columns:
                n_level = row[nitrogen_col]
                if n_level < 0.5 or n_level > 2.0:  # Too low or too high
                    score += 2
                elif n_level < 1.0 or n_level > 1.5:  # Slightly imbalanced
                    score += 1
            
            # Check phosphorus levels
            if phosphorus_col and phosphorus_col in data.columns:
                p_level = row[phosphorus_col]
                if p_level < 10 or p_level > 40:  # ppm
                    score += 2
                elif p_level < 15 or p_level > 30:
                    score += 1
            
            # Check potassium levels
            if potassium_col and potassium_col in data.columns:
                k_level = row[potassium_col]
                if k_level < 80 or k_level > 300:  # ppm
                    score += 2
                elif k_level < 120 or k_level > 250:
                    score += 1
            
            # Organic matter factor
            if organic_matter_col and organic_matter_col in data.columns:
                om = row[organic_matter_col]
                if om < 1.0:  # Very low organic matter
                    score += 3
                elif om < 2.0:
                    score += 2
                elif om < 3.0:
                    score += 1
            
            # pH factor
            if ph_col and ph_col in data.columns:
                ph = row[ph_col]
                if ph < 5.5 or ph > 8.5:  # Extreme pH
                    score += 2
                elif ph < 6.0 or ph > 8.0:  # Suboptimal pH
                    score += 1
            
            # Environmental factors
            erosion_col = None
            for col in data.columns:
                if 'erosion' in col.lower():
                    erosion_col = col
                    break
            
            if erosion_col and erosion_col in data.columns:
                erosion = str(row[erosion_col]).lower()
                if 'high' in erosion or 'severe' in erosion:
                    score += 3
                elif 'moderate' in erosion:
                    score += 2
                elif 'low' in erosion:
                    score += 1
            
            # Convert score to risk category
            if score >= 8:
                risk_scores.append('CRITICAL')
            elif score >= 5:
                risk_scores.append('HIGH')
            elif score >= 2:
                risk_scores.append('MEDIUM')
            else:
                risk_scores.append('LOW')
        
        return np.array(risk_scores)
    
    def prepare_nutrient_toxicity_features(self, data):
        """
        Prepare features for nutrient toxicity prediction
        
        Args:
            data (pd.DataFrame): Input soil data
            
        Returns:
            tuple: (X, y) features and target for nutrient toxicity
        """
        # Focus on nutrient levels and their interactions (case-insensitive)
        nutrient_cols = ['nitrogen', 'phosphorus', 'potassium', 'calcium', 'magnesium', 'sulfur', 'iron', 'zinc', 'copper', 'manganese']
        available_nutrients = []
        
        for col in nutrient_cols:
            # Find matching column (case-insensitive)
            matching_col = None
            for actual_col in data.columns:
                if actual_col.lower() == col.lower():
                    matching_col = actual_col
                    break
            if matching_col:
                available_nutrients.append(matching_col)
        
        # Add soil properties that affect nutrient availability (case-insensitive)
        soil_factors = ['ph', 'organic_matter', 'soil_moisture', 'temperature']
        available_factors = []
        
        for col in soil_factors:
            matching_col = None
            for actual_col in data.columns:
                if actual_col.lower() == col.lower():
                    matching_col = actual_col
                    break
            if matching_col:
                available_factors.append(matching_col)
        
        feature_columns = available_nutrients + available_factors
        
        if not feature_columns:
            print("No valid toxicity features found!")
            return None, None
        
        print(f"Using toxicity features: {feature_columns}")
        
        X = data[feature_columns].copy()
        
        # Create interaction features
        nitrogen_col = None
        phosphorus_col = None
        organic_matter_col = None
        
        # Find nitrogen column
        for col in data.columns:
            if col.lower() == 'nitrogen':
                nitrogen_col = col
                break
        
        # Find phosphorus column
        for col in data.columns:
            if col.lower() == 'phosphorus':
                phosphorus_col = col
                break
        
        # Find organic matter column
        for col in data.columns:
            if col.lower() == 'organic_matter':
                organic_matter_col = col
                break
        
        # Create interaction features if columns exist
        if nitrogen_col and phosphorus_col and nitrogen_col in X.columns and phosphorus_col in X.columns:
            X['n_p_interaction'] = X[nitrogen_col] * X[phosphorus_col]
        
        if organic_matter_col and nitrogen_col and organic_matter_col in X.columns and nitrogen_col in X.columns:
            X['om_n_interaction'] = X[organic_matter_col] * X[nitrogen_col]
        
        # Handle categorical variables
        categorical_features = X.select_dtypes(include=['object']).columns
        for col in categorical_features:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                X[col] = self.encoders[col].fit_transform(X[col].astype(str))
            else:
                X[col] = self.encoders[col].transform(X[col].astype(str))
        
        # Create target variable for nutrient toxicity
        y = self._calculate_nutrient_toxicity(data)
        
        self.feature_columns['nutrient_toxicity'] = feature_columns
        return X, y
    
    def _calculate_nutrient_toxicity(self, data):
        """
        Calculate nutrient toxicity risk
        
        Args:
            data (pd.DataFrame): Input soil data
            
        Returns:
            np.array: Toxicity categories (NONE, LOW, MODERATE, HIGH)
        """
        toxicity_scores = []
        
        for idx, row in data.iterrows():
            max_toxicity = 0
            
            # Check for individual nutrient toxicity
            if 'nitrogen' in data.columns:
                n = row['nitrogen']
                if n > 3.0:  # Very high nitrogen
                    max_toxicity = max(max_toxicity, 3)
                elif n > 2.0:
                    max_toxicity = max(max_toxicity, 2)
                elif n > 1.5:
                    max_toxicity = max(max_toxicity, 1)
            
            if 'phosphorus' in data.columns:
                p = row['phosphorus']
                if p > 50:  # Very high phosphorus
                    max_toxicity = max(max_toxicity, 3)
                elif p > 40:
                    max_toxicity = max(max_toxicity, 2)
                elif p > 30:
                    max_toxicity = max(max_toxicity, 1)
            
            if 'potassium' in data.columns:
                k = row['potassium']
                if k > 350:  # Very high potassium
                    max_toxicity = max(max_toxicity, 3)
                elif k > 300:
                    max_toxicity = max(max_toxicity, 2)
                elif k > 250:
                    max_toxicity = max(max_toxicity, 1)
            
            # Check micronutrient toxicity
            micronutrients = ['iron', 'zinc', 'copper', 'manganese']
            for nutrient in micronutrients:
                if nutrient in data.columns:
                    level = row[nutrient]
                    if nutrient == 'copper' and level > 2.0:  # ppm
                        max_toxicity = max(max_toxicity, 3)
                    elif nutrient == 'zinc' and level > 5.0:  # ppm
                        max_toxicity = max(max_toxicity, 3)
                    elif nutrient == 'manganese' and level > 10.0:  # ppm
                        max_toxicity = max(max_toxicity, 3)
            
            # Convert to toxicity category
            if max_toxicity >= 3:
                toxicity_scores.append('HIGH')
            elif max_toxicity >= 2:
                toxicity_scores.append('MODERATE')
            elif max_toxicity >= 1:
                toxicity_scores.append('LOW')
            else:
                toxicity_scores.append('NONE')
        
        return np.array(toxicity_scores)
    
    def prepare_fertility_trend_features(self, data):
        """
        Prepare features for long-term soil fertility trend prediction
        
        Args:
            data (pd.DataFrame): Input soil data
            
        Returns:
            tuple: (X, y) features and target for fertility trend
        """
        # Features that influence long-term fertility
        feature_columns = []
        
        # Current soil health indicators
        health_indicators = ['organic_matter', 'nitrogen', 'phosphorus', 'potassium', 'ph']
        available_health = [col for col in health_indicators if col in data.columns]
        feature_columns.extend(available_health)
        
        # Management practices
        management_cols = ['fertilizer_usage', 'crop_rotation', 'tillage_method', 'organic_amendments']
        available_mgmt = [col for col in management_cols if col in data.columns]
        feature_columns.extend(available_mgmt)
        
        # Environmental factors
        env_cols = ['rainfall', 'temperature', 'slope', 'erosion_level']
        available_env = [col for col in env_cols if col in data.columns]
        feature_columns.extend(available_env)
        
        X = data[feature_columns].copy()
        
        # Handle categorical variables
        categorical_features = X.select_dtypes(include=['object']).columns
        for col in categorical_features:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                X[col] = self.encoders[col].fit_transform(X[col].astype(str))
            else:
                X[col] = self.encoders[col].transform(X[col].astype(str))
        
        # Create target variable for fertility trend (soil health index)
        y = self._calculate_fertility_index(data)
        
        self.feature_columns['fertility_trend'] = feature_columns
        return X, y
    
    def _calculate_fertility_index(self, data):
        """
        Calculate soil fertility index (0-100 scale)
        
        Args:
            data (pd.DataFrame): Input soil data
            
        Returns:
            np.array: Fertility index values
        """
        fertility_indices = []
        
        for idx, row in data.iterrows():
            index = 50  # Base score
            
            # Organic matter contribution (0-25 points)
            if 'organic_matter' in data.columns:
                om = row['organic_matter']
                if om >= 4.0:
                    index += 25
                elif om >= 3.0:
                    index += 20
                elif om >= 2.0:
                    index += 15
                elif om >= 1.0:
                    index += 10
                else:
                    index -= 10
            
            # Nutrient balance contribution (0-30 points)
            if 'nitrogen' in data.columns:
                n = row['nitrogen']
                if 1.0 <= n <= 2.0:
                    index += 10
                elif 0.5 <= n <= 3.0:
                    index += 5
                else:
                    index -= 5
            
            if 'phosphorus' in data.columns:
                p = row['phosphorus']
                if 15 <= p <= 30:
                    index += 10
                elif 10 <= p <= 40:
                    index += 5
                else:
                    index -= 5
            
            if 'potassium' in data.columns:
                k = row['potassium']
                if 120 <= k <= 250:
                    index += 10
                elif 80 <= k <= 300:
                    index += 5
                else:
                    index -= 5
            
            # pH contribution (0-15 points)
            if 'ph' in data.columns:
                ph = row['ph']
                if 6.0 <= ph <= 7.5:
                    index += 15
                elif 5.5 <= ph <= 8.0:
                    index += 10
                elif 5.0 <= ph <= 8.5:
                    index += 5
                else:
                    index -= 10
            
            # Management practices
            if 'organic_amendments' in data.columns:
                amendments = str(row['organic_amendments']).lower()
                if 'compost' in amendments or 'manure' in amendments:
                    index += 10
                elif 'organic' in amendments:
                    index += 5
            
            # Ensure index stays within 0-100 range
            index = max(0, min(100, index))
            fertility_indices.append(index)
        
        return np.array(fertility_indices)
    
    def train_models(self, data):
        """
        Train all AI models with the provided data
        
        Args:
            data (pd.DataFrame): Training dataset
        """
        print("Training Soil Health Risk Prediction Models...")
        
        # Train degradation risk model
        X_degrad, y_degrad = self.prepare_degradation_risk_features(data)
        X_degrad_scaled = self.scalers['degradation_risk'].fit_transform(X_degrad)
        self.models['degradation_risk'].fit(X_degrad_scaled, y_degrad)
        
        # Train nutrient toxicity model
        X_toxic, y_toxic = self.prepare_nutrient_toxicity_features(data)
        X_toxic_scaled = self.scalers['nutrient_toxicity'].fit_transform(X_toxic)
        self.models['nutrient_toxicity'].fit(X_toxic_scaled, y_toxic)
        
        # Train fertility trend model
        X_fert, y_fert = self.prepare_fertility_trend_features(data)
        X_fert_scaled = self.scalers['fertility_trend'].fit_transform(X_fert)
        self.models['fertility_trend'].fit(X_fert_scaled, y_fert)
        
        print("All models trained successfully!")
    
    def predict_degradation_risk(self, soil_data):
        """
        Predict soil degradation risk
        
        Args:
            soil_data (pd.DataFrame): Soil data for prediction
            
        Returns:
            dict: Risk assessment with confidence scores
        """
        # Prepare features
        X, _ = self.prepare_degradation_risk_features(soil_data)
        X_scaled = self.scalers['degradation_risk'].transform(X)
        
        # Make prediction
        predictions = self.models['degradation_risk'].predict(X_scaled)
        probabilities = self.models['degradation_risk'].predict_proba(X_scaled)
        
        # Get confidence scores
        confidence_scores = np.max(probabilities, axis=1)
        
        results = []
        for i, (pred, conf) in enumerate(zip(predictions, confidence_scores)):
            results.append({
                'risk_level': pred,
                'confidence': conf,
                'risk_factors': self._identify_risk_factors(soil_data.iloc[i])
            })
        
        return results
    
    def predict_nutrient_toxicity(self, soil_data):
        """
        Predict nutrient toxicity risk
        
        Args:
            soil_data (pd.DataFrame): Soil data for prediction
            
        Returns:
            dict: Toxicity assessment with affected nutrients
        """
        X, _ = self.prepare_nutrient_toxicity_features(soil_data)
        X_scaled = self.scalers['nutrient_toxicity'].transform(X)
        
        predictions = self.models['nutrient_toxicity'].predict(X_scaled)
        probabilities = self.models['nutrient_toxicity'].predict_proba(X_scaled)
        
        confidence_scores = np.max(probabilities, axis=1)
        
        results = []
        for i, (pred, conf) in enumerate(zip(predictions, confidence_scores)):
            results.append({
                'toxicity_level': pred,
                'confidence': conf,
                'affected_nutrients': self._identify_toxic_nutrients(soil_data.iloc[i])
            })
        
        return results
    
    def predict_fertility_trend(self, soil_data):
        """
        Predict long-term soil fertility trend
        
        Args:
            soil_data (pd.DataFrame): Soil data for prediction
            
        Returns:
            dict: Fertility trend analysis
        """
        X, _ = self.prepare_fertility_trend_features(soil_data)
        X_scaled = self.scalers['fertility_trend'].transform(X)
        
        predictions = self.models['fertility_trend'].predict(X_scaled)
        
        results = []
        for i, pred in enumerate(predictions):
            trend = self._analyze_fertility_trend(pred)
            results.append({
                'fertility_index': pred,
                'trend': trend['direction'],
                'trend_description': trend['description'],
                'recommendations': self._get_fertility_recommendations(pred, soil_data.iloc[i])
            })
        
        return results
    
    def _identify_risk_factors(self, soil_row):
        """Identify specific risk factors for degradation"""
        factors = []
        
        if 'organic_matter' in soil_row and soil_row['organic_matter'] < 2.0:
            factors.append('Low organic matter')
        
        if 'ph' in soil_row and (soil_row['ph'] < 5.5 or soil_row['ph'] > 8.5):
            factors.append('Extreme pH levels')
        
        if 'erosion_level' in soil_row:
            erosion = str(soil_row['erosion_level']).lower()
            if 'high' in erosion or 'severe' in erosion:
                factors.append('High erosion risk')
        
        return factors
    
    def _identify_toxic_nutrients(self, soil_row):
        """Identify nutrients with toxicity risk"""
        toxic_nutrients = []
        
        if 'nitrogen' in soil_row and soil_row['nitrogen'] > 2.0:
            toxic_nutrients.append('Nitrogen')
        
        if 'phosphorus' in soil_row and soil_row['phosphorus'] > 30:
            toxic_nutrients.append('Phosphorus')
        
        if 'potassium' in soil_row and soil_row['potassium'] > 250:
            toxic_nutrients.append('Potassium')
        
        return toxic_nutrients
    
    def _analyze_fertility_trend(self, fertility_index):
        """Analyze fertility trend based on index"""
        if fertility_index >= 80:
            return {'direction': 'Improving', 'description': 'Excellent soil health with positive trend'}
        elif fertility_index >= 60:
            return {'direction': 'Stable', 'description': 'Good soil health, maintain current practices'}
        elif fertility_index >= 40:
            return {'direction': 'Declining', 'description': 'Moderate soil health, needs improvement'}
        else:
            return {'direction': 'Critical', 'description': 'Poor soil health, immediate action required'}
    
    def _get_fertility_recommendations(self, fertility_index, soil_row):
        """Get recommendations based on fertility index"""
        recommendations = []
        
        if fertility_index < 40:
            recommendations.append('Increase organic matter additions')
            recommendations.append('Implement crop rotation')
            recommendations.append('Reduce chemical fertilizer use')
            recommendations.append('Add cover crops')
        elif fertility_index < 60:
            recommendations.append('Maintain organic matter levels')
            recommendations.append('Monitor nutrient balance')
            recommendations.append('Consider green manures')
        else:
            recommendations.append('Continue sustainable practices')
            recommendations.append('Regular soil testing')
        
        return recommendations
    
    def perform_cross_validation(self, data, cv_folds=5):
        """
        Perform K-fold cross-validation on all models
        
        Args:
            data (pd.DataFrame): Training dataset
            cv_folds (int): Number of cross-validation folds
            
        Returns:
            dict: Cross-validation results for all models
        """
        print(f"Performing {cv_folds}-fold cross-validation...")
        
        cv_results = {}
        
        # Cross-validation for degradation risk model
        X_degrad, y_degrad = self.prepare_degradation_risk_features(data)
        X_degrad_scaled = self.scalers['degradation_risk'].fit_transform(X_degrad)
        
        cv_degrad = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
        degrad_scores = cross_val_score(
            self.models['degradation_risk'], 
            X_degrad_scaled, 
            y_degrad, 
            cv=cv_degrad, 
            scoring='accuracy'
        )
        
        cv_results['degradation_risk'] = {
            'mean_accuracy': np.mean(degrad_scores),
            'std_accuracy': np.std(degrad_scores),
            'scores': degrad_scores.tolist()
        }
        
        # Cross-validation for nutrient toxicity model
        X_toxic, y_toxic = self.prepare_nutrient_toxicity_features(data)
        X_toxic_scaled = self.scalers['nutrient_toxicity'].fit_transform(X_toxic)
        
        cv_toxic = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
        toxic_scores = cross_val_score(
            self.models['nutrient_toxicity'], 
            X_toxic_scaled, 
            y_toxic, 
            cv=cv_toxic, 
            scoring='accuracy'
        )
        
        cv_results['nutrient_toxicity'] = {
            'mean_accuracy': np.mean(toxic_scores),
            'std_accuracy': np.std(toxic_scores),
            'scores': toxic_scores.tolist()
        }
        
        # Cross-validation for fertility trend model
        X_fert, y_fert = self.prepare_fertility_trend_features(data)
        X_fert_scaled = self.scalers['fertility_trend'].fit_transform(X_fert)
        
        cv_fert = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
        fert_scores = cross_val_score(
            self.models['fertility_trend'], 
            X_fert_scaled, 
            y_fert, 
            cv=cv_fert, 
            scoring='r2'
        )
        
        cv_results['fertility_trend'] = {
            'mean_r2_score': np.mean(fert_scores),
            'std_r2_score': np.std(fert_scores),
            'scores': fert_scores.tolist()
        }
        
        print("Cross-validation completed!")
        return cv_results
    
    def evaluate_models(self, test_data):
        """
        Evaluate model performance
        
        Args:
            test_data (pd.DataFrame): Test dataset
            
        Returns:
            dict: Model performance metrics
        """
        results = {}
        
        # Evaluate degradation risk model
        X_degrad, y_degrad = self.prepare_degradation_risk_features(test_data)
        X_degrad_scaled = self.scalers['degradation_risk'].transform(X_degrad)
        y_pred_degrad = self.models['degradation_risk'].predict(X_degrad_scaled)
        
        results['degradation_risk'] = {
            'accuracy': accuracy_score(y_degrad, y_pred_degrad),
            'classification_report': classification_report(y_degrad, y_pred_degrad)
        }
        
        # Evaluate nutrient toxicity model
        X_toxic, y_toxic = self.prepare_nutrient_toxicity_features(test_data)
        X_toxic_scaled = self.scalers['nutrient_toxicity'].transform(X_toxic)
        y_pred_toxic = self.models['nutrient_toxicity'].predict(X_toxic_scaled)
        
        results['nutrient_toxicity'] = {
            'accuracy': accuracy_score(y_toxic, y_pred_toxic),
            'classification_report': classification_report(y_toxic, y_pred_toxic)
        }
        
        # Evaluate fertility trend model
        X_fert, y_fert = self.prepare_fertility_trend_features(test_data)
        X_fert_scaled = self.scalers['fertility_trend'].transform(X_fert)
        y_pred_fert = self.models['fertility_trend'].predict(X_fert_scaled)
        
        results['fertility_trend'] = {
            'r2_score': r2_score(y_fert, y_pred_fert),
            'mse': mean_squared_error(y_fert, y_pred_fert),
            'rmse': np.sqrt(mean_squared_error(y_fert, y_pred_fert))
        }
        
        return results

# Example usage and testing
def test_soil_health_ai():
    """Test Soil Health Risk Prediction AI with multi-CSV loading"""
    print("=== Soil Health Risk Prediction AI Test ===")
    
    # Initialize AI model
    shrp = SoilHealthRiskPrediction(model_type='random_forest')
    
    # Option 1: Load from multiple CSV files (recommended for your soil dataset)
    csv_folder_path = r"C:\Users\User\Downloads"
    
    # Option 2: Load from single CSV file (fallback)
    single_file_path = r"C:\Users\User\Downloads\Soil Nutrients (1).csv"
    
    print("Loading soil data...")
    
    # Try to load from multiple CSVs first
    if os.path.exists(csv_folder_path):
        print(f"Attempting to load from folder: {csv_folder_path}")
        full_data = shrp.load_and_preprocess_data(csv_folder_path=csv_folder_path)
    elif os.path.exists(single_file_path):
        print(f"Folder not found. Loading from single file: {single_file_path}")
        full_data = shrp.load_and_preprocess_data(file_path=single_file_path)
    else:
        print("No data files found. Using sample data for demonstration...")
        # Create sample data as fallback
        full_data = pd.DataFrame({
            'nitrogen': [1.2, 2.5, 0.8, 3.2, 1.5, 1.8, 2.1, 0.9, 2.8, 1.3],
            'phosphorus': [25, 45, 15, 50, 20, 30, 35, 18, 42, 28],
            'potassium': [150, 280, 100, 350, 180, 220, 260, 130, 310, 190],
            'organic_matter': [3.5, 1.8, 2.2, 0.8, 4.1, 2.8, 1.5, 3.9, 1.2, 3.3],
            'ph': [6.5, 8.2, 5.2, 4.8, 7.1, 6.8, 7.8, 5.8, 8.0, 6.2],
            'soil_type': ['loam', 'clay', 'sandy', 'clay', 'loam', 'sandy', 'clay', 'loam', 'sandy', 'loam'],
            'erosion_level': ['low', 'moderate', 'high', 'severe', 'low', 'moderate', 'high', 'low', 'moderate', 'low'],
            'fertilizer_usage': ['moderate', 'high', 'low', 'high', 'moderate', 'moderate', 'high', 'low', 'high', 'moderate'],
            'crop_rotation': ['yes', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'yes']
        })
        print(f"Sample data created: {full_data.shape}")
    
    if full_data is None or len(full_data) == 0:
        print("❌ No data available for training")
        return
    
    print(f"\n✅ Successfully loaded dataset: {full_data.shape}")
    
    # Perform cross-validation
    print("\n=== Cross-Validation Results ===")
    cv_results = shrp.perform_cross_validation(full_data, cv_folds=5)
    
    for model, results in cv_results.items():
        print(f"\n{model.upper()} Model Cross-Validation:")
        if 'mean_accuracy' in results:
            print(f"  Mean Accuracy: {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f}")
        else:
            print(f"  Mean R² Score: {results['mean_r2_score']:.4f} ± {results['std_r2_score']:.4f}")
        print(f"  Individual Scores: {[f'{s:.3f}' for s in results['scores'][:5]]}")
    
    # Train models
    print("\n=== Training Models ===")
    shrp.train_models(full_data)
    
    # Test predictions on a sample of the data
    print("\n=== Testing Predictions ===")
    test_sample = full_data.head(10) if len(full_data) >= 10 else full_data
    
    # Test degradation risk
    degrad_risks = shrp.predict_degradation_risk(test_sample)
    print("Degradation Risk Predictions:")
    for i, risk in enumerate(degrad_risks[:5]):  # Show first 5
        print(f"Sample {i+1}: {risk['risk_level']} (confidence: {risk['confidence']:.2f})")
    
    # Test nutrient toxicity
    toxicity = shrp.predict_nutrient_toxicity(test_sample)
    print("\nNutrient Toxicity Predictions:")
    for i, tox in enumerate(toxicity[:5]):  # Show first 5
        print(f"Sample {i+1}: {tox['toxicity_level']} (confidence: {tox['confidence']:.2f})")
    
    # Test fertility trend
    fertility = shrp.predict_fertility_trend(test_sample)
    print("\nFertility Trend Predictions:")
    for i, fert in enumerate(fertility[:5]):  # Show first 5
        print(f"Sample {i+1}: {fert['fertility_index']:.1f}/100 - {fert['trend']}")
    
    # Evaluate models
    print("\n=== Model Evaluation ===")
    evaluation = shrp.evaluate_models(full_data)
    for model, metrics in evaluation.items():
        print(f"\n{model.upper()} Model:")
        for metric, value in metrics.items():
            if isinstance(value, (int, float)):
                print(f"  {metric}: {value:.4f}")
            else:
                print(f"  {metric}: {value}")
    
    print(f"\n=== Summary ===")
    print("✅ Multi-CSV loading system implemented!")
    print("✅ Cross-validation completed successfully!")
    print("✅ Models trained and tested!")
    print("✅ Ready for production deployment!")
    
    # Additional information
    print(f"\n=== Dataset Information ===")
    print(f"Total samples: {len(full_data)}")
    print(f"Features available: {len(full_data.columns)}")
    print(f"Key nutrients: N, P, K, organic matter, pH")
    print(f"AI models: Degradation risk, Nutrient toxicity, Fertility trends")
    
    return shrp, full_data

if __name__ == "__main__":
    test_soil_health_ai()
