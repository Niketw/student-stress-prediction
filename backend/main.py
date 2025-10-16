from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from models.model import StressPredictor
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize paths
model_path = os.path.join(os.path.dirname(__file__), "models", "stress_predictor.joblib")
dataset_path = os.path.join(os.path.dirname(__file__), "dataset", "StressLevelDataset.csv")
predictor = None

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None

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
    recommendations: str

# Helper function to generate recommendations using Groq
async def generate_recommendations(features: dict, stress_category: str) -> str:
    """Generate personalized stress relief recommendations using Groq LLM"""
    
    if not groq_client:
        return "Unable to generate recommendations - Groq API not configured"
    
    # Create a detailed prompt based on user's stress factors
    prompt = f"""Based on the following student stress assessment data, provide 5-7 specific, actionable recommendations to help reduce stress:

**Stress Level**: {stress_category}

**Stress Factors Assessment**:
- Anxiety Level: {features['anxiety_level']}/10
- Depression: {features['depression']}/10
- Self-Esteem: {features['self_esteem']}/10
- Sleep Quality: {features['sleep_quality']}/10
- Academic Performance: {features['academic_performance']}/10
- Study Load: {features['study_load']}/10
- Social Support: {features['social_support']}/10
- Peer Pressure: {features['peer_pressure']}/10
- Mental Health History: {features['mental_health_history']}/10
- Living Conditions: {features['living_conditions']}/10
- Safety Feeling: {features['safety']}/10
- Breathing Problems: {features['breathing_problem']}/10
- Noise Level Exposure: {features['noise_level']}/10
- Bullying Exposure: {features['bullying']}/10

Please provide:
1. Immediate stress relief techniques
2. Sleep and lifestyle improvements
3. Academic and study strategies
4. Social support and relationships advice
5. Mental health resources recommendations

Keep recommendations practical, specific, and tailored to the student's specific stress factors. Format as clear, numbered list."""

    try:
        # Try available models in order
        models = [
            "llama-3.2-90b-vision-preview",
            "llama-3.1-8b-instant",
            "gemma-7b-it",
        ]
        
        message = None
        last_error = None
        
        for model in models:
            try:
                message = groq_client.chat.completions.create(
                    model=model,
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                break  # Success, exit loop
            except Exception as model_error:
                last_error = model_error
                continue  # Try next model
        
        if message is None:
            return f"All models failed. Last error: {str(last_error)}"
        
        content = message.choices[0].message.content
        return content if content else "Unable to generate recommendations at this time."
    except Exception as e:
        return f"Recommendations generation failed: {str(e)}"

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
        
        stress_category = stress_categories.get(prediction, "Unknown")
        
        # Generate recommendations using Groq
        recommendations = await generate_recommendations(features.dict(), stress_category)
        
        return PredictionResponse(
            stress_level=int(prediction),
            stress_category=stress_category,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-status")
async def model_status():
    return {
        "model_loaded": predictor is not None,
        "groq_api_configured": groq_client is not None and groq_api_key and groq_api_key != "your_groq_api_key_here"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)