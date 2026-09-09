from pathlib import Path
import pandas as pd
import joblib


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "Heart_Disease.pkl"


_model = None



def load_artifacts():
    global _model
    
    if _model is None:
        _model = joblib.load(MODEL_PATH)
        
        
    
def predict_heart_disease(payload: dict):
    
    load_artifacts()
    
    # Convert input data into DataFrame
    X = pd.DataFrame([payload])
    print('Before Encoding')
    print(X)

    
    # Prediction
    prediction = _model.predict(X)[0]
    
    # Prediction Probability
    probability = _model.predict_proba(X)[0][1]
    
    
    print("Prediction :", prediction)
    print('Probability:', probability)
    
    return {
        'prediction' : int(prediction),
        'probability' : float(probability)
    }


