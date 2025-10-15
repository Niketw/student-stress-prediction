from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from models.model import StressPredictor
import os

# Initialize paths
model_path = os.path.join(os.path.dirname(__file__), "models", "stress_predictor.joblib")
dataset_path = os.path.join(os.path.dirname(__file__), "dataset", "StressLevelDataset.csv")
predictor = None

# Train and load model immediately
def initialize_model():
    global predictor
    
    # Check if model exists
    if not os.path.exists(model_path):
        if os.path.exists(dataset_path):
            print("\n" + "="*50)
            print("Model not found. Training model...")
            print("="*50)
            try:
                from train import train_model
                train_model()
                print("="*50)
                print("Model training completed!")
                print("="*50 + "\n")
            except Exception as e:
                print(f"Error training model: {str(e)}")
                return False
        else:
            print(f"Dataset not found at {dataset_path}")
            return False
    
    # Load the model
    try:
        predictor = StressPredictor.load_model(model_path)
        print(f"✓ Model loaded successfully from {model_path}")
        return True
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        predictor = None
        return False

# Initialize model before creating app
initialize_model()

app = FastAPI(title="Student Stress Prediction API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue.js default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentFeatures(BaseModel):
    anxiety_level: int
    self_esteem: int
    mental_health_history: int
    depression: int
    headache: int
    blood_pressure: int
    sleep_quality: int
    breathing_problem: int
    noise_level: int
    living_conditions: int
    safety: int
    basic_needs: int
    academic_performance: int
    study_load: int
    teacher_student_relationship: int
    future_career_concerns: int
    social_support: int
    peer_pressure: int
    extracurricular_activities: int
    bullying: int

class PredictionResponse(BaseModel):
    stress_level: int
    stress_category: str

@app.post("/predict", response_model=PredictionResponse)
async def predict_stress(features: StudentFeatures):
    if predictor is None:
        raise HTTPException(status_code=500, detail="Model not trained. Please train the model first.")
    
    # Convert input features to DataFrame
    input_data = pd.DataFrame([features.dict()])
    
    # Make prediction
    try:
        prediction = predictor.predict(input_data)[0]
        
        # Map stress level to category
        stress_categories = {
            0: "Low Stress",
            1: "Medium Stress",
            2: "High Stress"
        }
        
        return PredictionResponse(
            stress_level=int(prediction),
            stress_category=stress_categories.get(prediction, "Unknown")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-status")
async def model_status():
    return {"model_loaded": predictor is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)