import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from django.conf import settings

def generate_mock_training_data():
    """Generate mock training data for demonstration"""
    np.random.seed(42)
    n_samples = 1000
    
    # Mock features
    aod = np.random.uniform(0.1, 1.5, n_samples)
    temperature = np.random.uniform(15, 40, n_samples)
    humidity = np.random.uniform(30, 95, n_samples)
    wind_speed = np.random.uniform(0, 15, n_samples)
    
    # Mock target (PM2.5) with some relationship to features
    pm2_5 = (
        50 * aod + 
        0.5 * temperature + 
        0.2 * humidity - 
        1.5 * wind_speed + 
        np.random.normal(0, 10, n_samples)
    )
    pm2_5 = np.clip(pm2_5, 10, 500)  # Ensure realistic range
    
    # Create DataFrame
    data = pd.DataFrame({
        'aod': aod,
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'pm2_5': pm2_5
    })
    
    return data

def train_and_save_model():
    """Train Random Forest model and save it"""
    # Get training data
    df = generate_mock_training_data()
    
    # Split into features and target
    X = df[['aod', 'temperature', 'humidity', 'wind_speed']]
    y = df['pm2_5']
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Model Evaluation:")
    print(f"MSE: {mse:.2f}")
    print(f"R2 Score: {r2:.2f}")
    
    # Save model
    model_dir = os.path.join(settings.BASE_DIR, 'pollution_app/ml_model')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'trained_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()