"""
Comprehensive Soil AI Trainer
Uses ALL datasets and compares ALL ML models for SoilDoctor system
"""

import pandas as pd
import numpy as np
import glob
import os
import requests
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ML Models
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score, accuracy_score

class ComprehensiveSoilAITrainer:
    """Comprehensive AI trainer using all datasets and models"""
    
    def __init__(self):
        self.all_models = {}
        self.all_results = {}
        self.datasets = {}
        self.scalers = {}
        self.encoders = {}
        
        # Initialize all model types
        self._initialize_all_models()
        
        # Data sources
        self.csv_folder = r"C:\Users\User\Downloads"
        self.isda_api_url = "https://api.isda-africa.com/isdasoil/v2"
        self.api_token = None
    
    def _initialize_all_models(self):
        """Initialize all ML models for comparison"""
        
        # Random Forest models
        self.all_models['random_forest'] = {
            'degradation_risk': RandomForestClassifier(n_estimators=100, random_state=42),
            'nutrient_toxicity': RandomForestClassifier(n_estimators=100, random_state=42),
            'fertility_trend': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        # Gradient Boosting models
        self.all_models['gradient_boosting'] = {
            'degradation_risk': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'nutrient_toxicity': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'fertility_trend': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        # Decision Tree models
        self.all_models['decision_tree'] = {
            'degradation_risk': DecisionTreeClassifier(random_state=42),
            'nutrient_toxicity': DecisionTreeClassifier(random_state=42),
            'fertility_trend': DecisionTreeRegressor(random_state=42)
        }
        
        # Initialize scalers for each model type
        for model_type in self.all_models.keys():
            self.scalers[model_type] = {
                'degradation_risk': StandardScaler(),
                'nutrient_toxicity': StandardScaler(),
                'fertility_trend': StandardScaler()
            }
    
    def load_all_csv_datasets(self):
        """Load ALL CSV files from the Downloads folder"""
        print("=== Loading All CSV Datasets ===")
        
        # Find all CSV files
        all_csvs = glob.glob(os.path.join(self.csv_folder, '*.csv'))
        
        if not all_csvs:
            print("No CSV files found!")
            return {}
        
        print(f"Found {len(all_csvs)} CSV files:")
        for csv_file in all_csvs:
            print(f"  - {os.path.basename(csv_file)}")
        
        # Load each CSV file
        loaded_datasets = {}
        
        for csv_file in all_csvs:
            try:
                print(f"\nLoading: {os.path.basename(csv_file)}")
                df = pd.read_csv(csv_file)
                
                # Basic info
                print(f"  Shape: {df.shape}")
                print(f"  Columns: {list(df.columns)[:10]}...")  # Show first 10 columns
                
                # Check if it has soil-related columns
                soil_columns = self._identify_soil_columns(df)
                if soil_columns:
                    print(f"  ✓ Soil columns found: {soil_columns}")
                    loaded_datasets[os.path.basename(csv_file)] = df
                else:
                    print(f"  ⚠ No soil columns found, skipping")
                    
            except Exception as e:
                print(f"  ✗ Error loading {csv_file}: {e}")
                continue
        
        print(f"\n✅ Successfully loaded {len(loaded_datasets)} soil datasets")
        return loaded_datasets
    
    def _identify_soil_columns(self, df):
        """Identify soil-related columns in a DataFrame"""
        soil_keywords = [
            'nitrogen', 'phosphorus', 'potassium', 'ph', 'organic_matter',
            'soil', 'nutrient', 'fertility', 'texture', 'moisture', 'temperature',
            'rainfall', 'erosion', 'yield', 'crop'
        ]
        
        found_columns = []
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in soil_keywords):
                found_columns.append(col)
        
        return found_columns
    
    def authenticate_isda_api(self, email, password):
        """Authenticate with iSDA API"""
        try:
            auth_url = f"https://api.isda-africa.com/login"
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
                self.api_token = auth_data.get('access_token')
                print("✅ Successfully authenticated with iSDA API")
                return True
            else:
                print(f"❌ iSDA API authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ iSDA API authentication error: {e}")
            return False
    
    def fetch_isda_sample_data(self, locations=None):
        """Fetch sample data from iSDA API"""
        if not self.api_token:
            print("❌ Not authenticated with iSDA API")
            return None
        
        # Default locations if none provided (Kenya regions)
        if not locations:
            locations = [
                (-1.2921, 36.8219),  # Nairobi
                (-0.0236, 37.9062),  # Meru
                (-1.0669, 34.7492),  # Mwanza
                (-4.0435, 39.6682),  # Mombasa
                (0.5167, 35.2831)   # Eldoret
            ]
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "accept": "application/json"
        }
        
        all_isda_data = []
        
        for i, (lat, lon) in enumerate(locations):
            try:
                print(f"Fetching iSDA data for location {i+1}/{len(locations)}: ({lat}, {lon})")
                
                # Query soil properties
                soil_url = f"{self.isda_api_url}/soilproperty"
                params = {
                    "lat": lat,
                    "lon": lon
                }
                
                response = requests.get(soil_url, headers=headers, params=params)
                
                if response.status_code == 200:
                    soil_data = response.json()
                    
                    # Convert to DataFrame format
                    if 'property' in soil_data:
                        record = {
                            'latitude': lat,
                            'longitude': lon,
                            'source': 'iSDA_API',
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        # Add soil properties
                        props = soil_data['property']
                        for key, value in props.items():
                            if isinstance(value, list) and len(value) > 0:
                                item = value[0]
                                if 'value' in item:
                                    record[key] = item['value']
                                else:
                                    record[key] = item
                            else:
                                record[key] = value
                        
                        # Map iSDA properties to match CSV column names
                        mapped_record = self._map_isda_to_csv_format(record)
                        all_isda_data.append(mapped_record)
                        print(f"  ✓ Retrieved data for ({lat}, {lon})")
                    else:
                        print(f"  ⚠ No properties data for ({lat}, {lon})")
                else:
                    print(f"  ✗ API request failed: {response.status_code}")
                    
            except Exception as e:
                print(f"  ✗ Error fetching data for ({lat}, {lon}): {e}")
                continue
        
        if all_isda_data:
            isda_df = pd.DataFrame(all_isda_data)
            print(f"✅ Retrieved iSDA data: {isda_df.shape}")
            return isda_df
        else:
            print("❌ No iSDA data retrieved")
            return None
    
    def _map_isda_to_csv_format(self, isda_record):
        """Map iSDA API properties to match CSV column names"""
        mapped = isda_record.copy()
        
        # Map iSDA properties to CSV column names
        property_mapping = {
            'ph': 'pH',
            'nitrogen_total': 'Nitrogen',
            'phosphorous_extractable': 'Phosphorus',
            'potassium_extractable': 'Potassium',
            'aluminium_extractable': 'Aluminium',
            'organic_carbon': 'Organic_Matter',
            'clay_content': 'Clay',
            'silt_content': 'Silt',
            'sand_content': 'Sand',
            'bulk_density': 'Bulk_Density',
            'electrical_conductivity': 'EC',
            'cation_exchange_capacity': 'CEC'
        }
        
        # Apply mapping
        for isda_key, csv_key in property_mapping.items():
            if isda_key in mapped:
                mapped[csv_key] = mapped[isda_key]
        
        # Add missing columns with default values to match CSV format
        required_columns = ['Temperature', 'Rainfall', 'Fertility', 'Photoperiod', 'Light_Hours', 
                        'Light_Intensity', 'Rh', 'Yield', 'Category_pH', 'Soil_Type']
        
        for col in required_columns:
            if col not in mapped:
                # Add reasonable default values for demonstration
                if col == 'Temperature':
                    mapped[col] = 25.0  # Average temperature
                elif col == 'Rainfall':
                    mapped[col] = 1000.0  # Average rainfall
                elif col == 'Fertility':
                    mapped[col] = 'Medium'
                elif col == 'Photoperiod':
                    mapped[col] = 12.0
                elif col == 'Light_Hours':
                    mapped[col] = 8.0
                elif col == 'Light_Intensity':
                    mapped[col] = 50000.0
                elif col == 'Rh':
                    mapped[col] = 65.0
                elif col == 'Yield':
                    mapped[col] = 2.5
                elif col == 'Category_pH':
                    if 'pH' in mapped:
                        ph_val = mapped['pH']
                        if ph_val < 6.0:
                            mapped[col] = 'Acidic'
                        elif ph_val < 7.5:
                            mapped[col] = 'Neutral'
                        else:
                            mapped[col] = 'Alkaline'
                    else:
                        mapped[col] = 'Neutral'
                elif col == 'Soil_Type':
                    mapped[col] = 'Loam'
        
        return mapped
    
    def combine_all_datasets(self, csv_datasets, isda_data=None):
        """Combine all datasets into one comprehensive dataset"""
        print("\n=== Combining All Datasets ===")
        
        all_dataframes = []
        
        # Add CSV datasets
        for name, df in csv_datasets.items():
            # Add source column
            df_copy = df.copy()
            df_copy['data_source'] = f'CSV_{name.replace(".csv", "")}'
            all_dataframes.append(df_copy)
            print(f"  ✓ Added {name}: {df.shape}")
        
        # Add iSDA data if available
        if isda_data is not None:
            isda_data['data_source'] = 'iSDA_API'
            all_dataframes.append(isda_data)
            print(f"  ✓ Added iSDA API data: {isda_data.shape}")
        
        if not all_dataframes:
            print("❌ No datasets to combine")
            return None
        
        # Combine all datasets
        try:
            combined_data = pd.concat(all_dataframes, ignore_index=True, sort=False)
            print(f"\n✅ Combined dataset shape: {combined_data.shape}")
            print(f"✅ Total records: {len(combined_data)}")
            print(f"✅ Total columns: {len(combined_data.columns)}")
            
            # Show data sources
            print(f"\nData sources:")
            print(combined_data['data_source'].value_counts())
            
            return combined_data
            
        except Exception as e:
            print(f"❌ Error combining datasets: {e}")
            return None
    
    def prepare_features_for_all_models(self, data):
        """Prepare features for all model types"""
        print("\n=== Preparing Features for All Models ===")
        
        # Identify available soil columns
        soil_columns = self._identify_soil_columns(data)
        print(f"Available soil columns: {soil_columns}")
        
        # Create feature sets for different model types
        feature_sets = {}
        
        # Find numeric soil columns
        numeric_soil_cols = []
        for col in soil_columns:
            if col in data.columns and data[col].dtype in ['int64', 'float64']:
                numeric_soil_cols.append(col)
        
        # Find categorical soil columns
        categorical_soil_cols = []
        for col in soil_columns:
            if col in data.columns and data[col].dtype == 'object':
                categorical_soil_cols.append(col)
        
        print(f"Numeric soil columns: {numeric_soil_cols}")
        print(f"Categorical soil columns: {categorical_soil_cols}")
        
        # Prepare features for each model type
        for model_type in self.all_models.keys():
            feature_sets[model_type] = {
                'numeric_features': numeric_soil_cols.copy(),
                'categorical_features': categorical_soil_cols.copy(),
                'all_features': numeric_soil_cols + categorical_soil_cols
            }
        
        return feature_sets
    
    def create_target_variables(self, data):
        """Create target variables for all three prediction tasks"""
        print("\n=== Creating Target Variables ===")
        
        targets = {}
        
        # 1. Degradation Risk (Classification)
        degradation_risks = []
        for idx, row in data.iterrows():
            score = 0
            
            # Check nitrogen levels
            nitrogen_col = self._find_column_by_keyword(data, 'nitrogen')
            if nitrogen_col and nitrogen_col in data.columns:
                n_level = row[nitrogen_col]
                if n_level < 0.5 or n_level > 2.0:
                    score += 2
                elif n_level < 1.0 or n_level > 1.5:
                    score += 1
            
            # Check phosphorus levels
            phosphorus_col = self._find_column_by_keyword(data, 'phosphorus')
            if phosphorus_col and phosphorus_col in data.columns:
                p_level = row[phosphorus_col]
                if p_level < 10 or p_level > 40:
                    score += 2
                elif p_level < 15 or p_level > 30:
                    score += 1
            
            # Check potassium levels
            potassium_col = self._find_column_by_keyword(data, 'potassium')
            if potassium_col and potassium_col in data.columns:
                k_level = row[potassium_col]
                if k_level < 80 or k_level > 300:
                    score += 2
                elif k_level < 120 or k_level > 250:
                    score += 1
            
            # Check pH levels
            ph_col = self._find_column_by_keyword(data, 'ph')
            if ph_col and ph_col in data.columns:
                ph = row[ph_col]
                if ph < 5.5 or ph > 8.5:
                    score += 2
                elif ph < 6.0 or ph > 8.0:
                    score += 1
            
            # Convert score to risk category
            if score >= 8:
                degradation_risks.append('CRITICAL')
            elif score >= 5:
                degradation_risks.append('HIGH')
            elif score >= 2:
                degradation_risks.append('MEDIUM')
            else:
                degradation_risks.append('LOW')
        
        targets['degradation_risk'] = np.array(degradation_risks)
        
        # 2. Nutrient Toxicity (Classification)
        toxicity_levels = []
        for idx, row in data.iterrows():
            max_toxicity = 0
            
            # Check nitrogen toxicity (adjusted for your data range: 41-410)
            nitrogen_col = self._find_column_by_keyword(data, 'nitrogen')
            if nitrogen_col and nitrogen_col in data.columns:
                n = row[nitrogen_col]
                if n > 300:  # Very high for your data
                    max_toxicity = max(max_toxicity, 3)
                elif n > 200:  # High for your data
                    max_toxicity = max(max_toxicity, 2)
                elif n > 100:  # Moderate for your data
                    max_toxicity = max(max_toxicity, 1)
            
            # Check phosphorus toxicity (adjusted for your data range: 13-360)
            phosphorus_col = self._find_column_by_keyword(data, 'phosphorus')
            if phosphorus_col and phosphorus_col in data.columns:
                p = row[phosphorus_col]
                if p > 250:  # Very high for your data
                    max_toxicity = max(max_toxicity, 3)
                elif p > 180:  # High for your data
                    max_toxicity = max(max_toxicity, 2)
                elif p > 100:  # Moderate for your data
                    max_toxicity = max(max_toxicity, 1)
            
            # Check potassium toxicity (adjusted for your data range: 34-580)
            potassium_col = self._find_column_by_keyword(data, 'potassium')
            if potassium_col and potassium_col in data.columns:
                k = row[potassium_col]
                if k > 400:  # Very high for your data
                    max_toxicity = max(max_toxicity, 3)
                elif k > 300:  # High for your data
                    max_toxicity = max(max_toxicity, 2)
                elif k > 200:  # Moderate for your data
                    max_toxicity = max(max_toxicity, 1)
            
            # Convert to toxicity category
            if max_toxicity >= 3:
                toxicity_levels.append('HIGH')
            elif max_toxicity >= 2:
                toxicity_levels.append('MODERATE')
            elif max_toxicity >= 1:
                toxicity_levels.append('LOW')
            else:
                toxicity_levels.append('NONE')
        
        targets['nutrient_toxicity'] = np.array(toxicity_levels)
        
        # 3. Fertility Index (Regression)
        fertility_indices = []
        for idx, row in data.iterrows():
            index = 50  # Base score
            
            # Nitrogen contribution
            nitrogen_col = self._find_column_by_keyword(data, 'nitrogen')
            if nitrogen_col and nitrogen_col in data.columns:
                n = row[nitrogen_col]
                if 1.0 <= n <= 2.0:
                    index += 10
                elif 0.5 <= n <= 3.0:
                    index += 5
                else:
                    index -= 5
            
            # Phosphorus contribution
            phosphorus_col = self._find_column_by_keyword(data, 'phosphorus')
            if phosphorus_col and phosphorus_col in data.columns:
                p = row[phosphorus_col]
                if 15 <= p <= 30:
                    index += 10
                elif 10 <= p <= 40:
                    index += 5
                else:
                    index -= 5
            
            # Potassium contribution
            potassium_col = self._find_column_by_keyword(data, 'potassium')
            if potassium_col and potassium_col in data.columns:
                k = row[potassium_col]
                if 120 <= k <= 250:
                    index += 10
                elif 80 <= k <= 300:
                    index += 5
                else:
                    index -= 5
            
            # pH contribution
            ph_col = self._find_column_by_keyword(data, 'ph')
            if ph_col and ph_col in data.columns:
                ph = row[ph_col]
                if 6.0 <= ph <= 7.5:
                    index += 15
                elif 5.5 <= ph <= 8.0:
                    index += 10
                elif 5.0 <= ph <= 8.5:
                    index += 5
                else:
                    index -= 10
            
            # Ensure index stays within 0-100 range
            index = max(0, min(100, index))
            fertility_indices.append(index)
        
        targets['fertility_trend'] = np.array(fertility_indices)
        
        # Print target distributions
        for target_name, target_values in targets.items():
            print(f"\n{target_name.upper()} distribution:")
            if target_name == 'fertility_trend':
                print(f"  Mean: {np.mean(target_values):.2f}")
                print(f"  Std: {np.std(target_values):.2f}")
                print(f"  Min: {np.min(target_values):.2f}")
                print(f"  Max: {np.max(target_values):.2f}")
            else:
                unique, counts = np.unique(target_values, return_counts=True)
                for category, count in zip(unique, counts):
                    print(f"  {category}: {count} ({count/len(target_values)*100:.1f}%)")
        
        return targets
    
    def _find_column_by_keyword(self, data, keyword):
        """Find column by keyword (case-insensitive)"""
        for col in data.columns:
            if col.lower() == keyword.lower():
                return col
        return None
    
    def train_all_models(self, combined_data, targets, feature_sets):
        """Train all models and compare performance"""
        print("\n=== Training All Models ===")
        
        results = {}
        
        for model_type, models in self.all_models.items():
            print(f"\n--- Training {model_type.upper()} Models ---")
            
            model_results = {}
            
            for task_name, model in models.items():
                print(f"\nTraining {task_name} model...")
                
                # Get features for this task
                features = feature_sets[model_type]['all_features']
                if not features:
                    print(f"  ⚠ No features available for {task_name}")
                    continue
                
                # Prepare data
                X = combined_data[features].copy()
                y = targets[task_name]
                
                # Handle categorical variables
                categorical_features = X.select_dtypes(include=['object']).columns
                for col in categorical_features:
                    if col not in self.encoders:
                        self.encoders[col] = LabelEncoder()
                        X[col] = self.encoders[col].fit_transform(X[col].astype(str))
                    else:
                        X[col] = self.encoders[col].transform(X[col].astype(str))
                
                # Handle missing values
                X = X.fillna(X.median())
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42, stratify=y if task_name != 'fertility_trend' else None
                )
                
                # Scale features
                X_train_scaled = self.scalers[model_type][task_name].fit_transform(X_train)
                X_test_scaled = self.scalers[model_type][task_name].transform(X_test)
                
                try:
                    # Train model
                    model.fit(X_train_scaled, y_train)
                    
                    # Make predictions
                    y_pred = model.predict(X_test_scaled)
                    
                    # Evaluate
                    if task_name == 'fertility_trend':
                        # Regression metrics
                        r2 = r2_score(y_test, y_pred)
                        mse = mean_squared_error(y_test, y_pred)
                        rmse = np.sqrt(mse)
                        
                        model_results[task_name] = {
                            'r2_score': r2,
                            'mse': mse,
                            'rmse': rmse,
                            'model': model
                        }
                        
                        print(f"  ✓ R² Score: {r2:.4f}")
                        print(f"  ✓ RMSE: {rmse:.4f}")
                        
                    else:
                        # Classification metrics
                        accuracy = accuracy_score(y_test, y_pred)
                        
                        model_results[task_name] = {
                            'accuracy': accuracy,
                            'model': model
                        }
                        
                        print(f"  ✓ Accuracy: {accuracy:.4f}")
                    
                    print(f"  ✓ {task_name} model trained successfully")
                    
                except Exception as e:
                    print(f"  ✗ Error training {task_name} model: {e}")
                    continue
            
            results[model_type] = model_results
        
        return results
    
    def compare_all_models(self, results):
        """Compare performance of all models"""
        print("\n" + "="*60)
        print("MODEL COMPARISON RESULTS")
        print("="*60)
        
        comparison_data = []
        
        for model_type, model_results in results.items():
            for task_name, metrics in model_results.items():
                comparison_data.append({
                    'Model': model_type.upper(),
                    'Task': task_name.replace('_', ' ').title(),
                    'Metric': 'R² Score' if task_name == 'fertility_trend' else 'Accuracy',
                    'Value': metrics.get('r2_score', metrics.get('accuracy', 0))
                })
        
        # Create comparison table
        comparison_df = pd.DataFrame(comparison_data)
        
        # Pivot for better display
        pivot_table = comparison_df.pivot_table(
            index='Model', 
            columns='Task', 
            values='Value',
            aggfunc='mean'
        )
        
        print("\nPerformance Comparison:")
        print(pivot_table.round(4))
        
        # Find best model for each task
        print(f"\n{'='*40}")
        print("BEST MODELS FOR EACH TASK")
        print(f"{'='*40}")
        
        for task in ['Degradation Risk', 'Nutrient Toxicity', 'Fertility Trend']:
            task_data = comparison_df[comparison_df['Task'] == task]
            if not task_data.empty:
                best_model = task_data.loc[task_data['Value'].idxmax()]
                print(f"{task}: {best_model['Model']} ({best_model['Value']:.4f})")
        
        return comparison_df, pivot_table
    
    def run_comprehensive_training(self, isda_email=None, isda_password=None):
        """Run the complete comprehensive training pipeline"""
        print("🚀 STARTING COMPREHENSIVE SOIL AI TRAINING")
        print("="*60)
        
        # Step 1: Load all CSV datasets
        csv_datasets = self.load_all_csv_datasets()
        
        # Step 2: Fetch iSDA API data (if credentials provided)
        isda_data = None
        if isda_email and isda_password:
            print("\n=== Fetching iSDA API Data ===")
            if self.authenticate_isda_api(isda_email, isda_password):
                isda_data = self.fetch_isda_sample_data()
        
        # Step 3: Combine all datasets
        combined_data = self.combine_all_datasets(csv_datasets, isda_data)
        
        if combined_data is None:
            print("❌ No data available for training")
            return None
        
        # Step 4: Prepare features
        feature_sets = self.prepare_features_for_all_models(combined_data)
        
        # Step 5: Create target variables
        targets = self.create_target_variables(combined_data)
        
        # Step 6: Train all models
        results = self.train_all_models(combined_data, targets, feature_sets)
        
        # Step 7: Compare models
        comparison_df, pivot_table = self.compare_all_models(results)
        
        # Step 8: Summary
        print(f"\n{'='*60}")
        print("TRAINING SUMMARY")
        print(f"{'='*60}")
        print(f"Total datasets used: {len(csv_datasets)}")
        if isda_data is not None:
            print(f"+ iSDA API data: {isda_data.shape[0]} records")
        print(f"Combined dataset: {combined_data.shape}")
        print(f"Models trained: {len(self.all_models)}")
        print(f"Tasks completed: {len(targets)}")
        
        print(f"\n✅ Comprehensive training completed successfully!")
        
        return {
            'combined_data': combined_data,
            'results': results,
            'comparison': comparison_df,
            'pivot_table': pivot_table,
            'feature_sets': feature_sets,
            'targets': targets
        }

# Main execution function
def main():
    """Main function to run comprehensive training"""
    trainer = ComprehensiveSoilAITrainer()
    
    # Run training (add your iSDA credentials if available)
    results = trainer.run_comprehensive_training(
        isda_email="matarasteve15@gmail.com",
        isda_password="Matara@123"
    )
    
    if results:
        print(f"\n🎉 Training completed! Best models identified.")
        print(f"📊 Check the comparison table above for detailed results.")
        
        # Save results
        comparison_file = os.path.join(os.getcwd(), 'model_comparison_results.csv')
        pivot_file = os.path.join(os.getcwd(), 'model_performance_summary.csv')
        results['comparison'].to_csv(comparison_file, index=False)
        results['pivot_table'].to_csv(pivot_file)
        print(f"📁 Results saved to:")
        print(f"   - {comparison_file}")
        print(f"   - {pivot_file}")
    
    return results

if __name__ == "__main__":
    main()
