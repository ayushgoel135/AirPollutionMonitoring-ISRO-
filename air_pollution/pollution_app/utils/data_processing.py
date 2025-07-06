import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from django.conf import settings

class PMPredictionModel:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(settings.BASE_DIR, 'pollution_app/ml_model/trained_model.pkl')
        
    def prepare_training_data(self):
        """Prepare training data from database"""
        # In a real implementation, you would fetch and join data from SatelliteData,
        # GroundMeasurement, and AtmosphericData models
        # For demo, we'll create mock data
        
        # Mock data with AOD, meteorological parameters, and PM2.5
        data = {
            'aod': np.random.uniform(0.1, 1.0, 100),
            'temperature': np.random.uniform(15, 35, 100),
            'humidity': np.random.uniform(30, 90, 100),
            'wind_speed': np.random.uniform(0, 10, 100),
            'pm2_5': np.random.uniform(10, 300, 100)
        }
        
        df = pd.DataFrame(data)
        return df
    
    def train_model(self):
        """Train Random Forest regression model"""
        df = self.prepare_training_data()
        
        # Features and target
        X = df[['aod', 'temperature', 'humidity', 'wind_speed']]
        y = df['pm2_5']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"Model trained - MSE: {mse:.2f}, R2: {r2:.2f}")
        
        # Save model
        joblib.dump(self.model, self.model_path)
    
    def load_model(self):
        """Load trained model"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False
    
    def predict_pm(self, aod, temp, humidity, wind_speed):
        """Predict PM2.5 from input features"""
        if self.model is None:
            if not self.load_model():
                self.train_model()
        
        # Create input array
        X = pd.DataFrame([[aod, temp, humidity, wind_speed]],
                         columns=['aod', 'temperature', 'humidity', 'wind_speed'])
        
        # Predict
        prediction = self.model.predict(X)
        return prediction[0]