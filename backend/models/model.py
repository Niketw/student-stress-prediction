import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import joblib

class StressPredictor:
    def __init__(self):
        self.scaler = None
        self.pca = None
        self.model = None
        
    def fit(self, X, y):
        # Scale the features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply PCA
        # Find number of components that explain 95% variance
        pca_temp = PCA()
        pca_temp.fit(X_scaled)
        cumulative_variance_ratio = np.cumsum(pca_temp.explained_variance_ratio_)
        n_components = np.argmax(cumulative_variance_ratio >= 0.95) + 1
        
        # Fit PCA with optimal components
        self.pca = PCA(n_components=n_components)
        X_pca = self.pca.fit_transform(X_scaled)
        
        # Train KNN model with optimal k=5 (from notebook)
        self.model = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
        self.model.fit(X_pca, y)
        
    def predict(self, X):
        # Check if model components are initialized
        if self.scaler is None or self.pca is None or self.model is None:
            raise ValueError("Model is not trained. Call fit() before making predictions.")
            
        # Transform new data
        X_scaled = self.scaler.transform(X)
        X_pca = self.pca.transform(X_scaled)
        
        # Make prediction
        return self.model.predict(X_pca)
    
    def save_model(self, filepath):
        model_data = {
            'scaler': self.scaler,
            'pca': self.pca,
            'model': self.model
        }
        joblib.dump(model_data, filepath)
    
    @classmethod
    def load_model(cls, filepath):
        predictor = cls()
        model_data = joblib.load(filepath)
        predictor.scaler = model_data['scaler']
        predictor.pca = model_data['pca']
        predictor.model = model_data['model']
        return predictor