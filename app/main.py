from fastapi import FastAPI
from contextlib import asynccontextmanager
from .schemas import HeartDiseaseInput, HeartDiseasePrediction
from .model_service import load_artifacts, predict_heart_disease


# Lifespan Handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Load the model
    load_artifacts()
    
    # Close the model and clean everythings
    yield


app = FastAPI(title= "Heart Disease Predictor", version= '2.2', lifespan=lifespan)

    
    
@app.get('/')
def home_page():
    return {
        'message': 'Welcome to our app',
        'success': True
    }
    
    
@app.post("/predict", response_model= HeartDiseasePrediction)
def get_prediction(features: HeartDiseaseInput):
    
    result = predict_heart_disease(features.model_dump())
    
    return HeartDiseasePrediction(
        HeartDisease=result["prediction"],
        probability= result['probability']
        )
    