import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from models.model import StressPredictor

def train_model():
    """Train and save the stress prediction model"""
    
    # Define paths
    dataset_path = 'dataset/StressLevelDataset.csv'
    model_path = 'models/stress_predictor.joblib'
    
    # Check if model already exists
    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}")
        return
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return
    
    print("Loading dataset...")
    df = pd.read_csv(dataset_path)
    
    print("Data preprocessing...")
    # Handle missing values
    for column in df.columns:
        if df[column].isnull().any():
            df[column].fillna(df[column].median(), inplace=True)
    
    # Handle outliers using IQR method
    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns
    for column in numerical_columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
    
    print("Separating features and target...")
    X = df.drop('stress_level', axis=1)
    y = df['stress_level']
    
    print(f"Training data shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Classes: {y.unique()}")
    
    print("Training model...")
    predictor = StressPredictor()
    predictor.fit(X, y)
    
    print(f"Saving model to {model_path}...")
    predictor.save_model(model_path)
    print("Model training completed successfully!")

if __name__ == "__main__":
    train_model()
