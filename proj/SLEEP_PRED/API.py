from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Input model
class SleepData(BaseModel):
    Age: float
    Gender: str
    Coffee_Intake: float
    Caffeine_mg: float
    Sleep_Hours: float
    BMI: float
    Heart_Rate: float
    Stress_Level: str
    Physical_Activity_Hours: float
    Health_Issues: str
    Occupation: str
    Smoking: float
    Alcohol_Consumption: float

# Load full pipeline (preprocessing + classifier)
clf = joblib.load(r"C:\Users\Z.S computers\Desktop\fastapi\APIS\apis\sleep_quality_pipeline.pkl")

# Create FastAPI app
app = FastAPI(title="Sleep Quality Prediction API")

@app.post("/predict")
def predict(input_data: SleepData):
    try:
        # Convert Pydantic model to DataFrame (v2)
        df = pd.DataFrame([input_data.model_dump()])
        
        # Predict with the full pipeline
        prediction = clf.predict(df)
        
        # Return only the predicted class
        return {"prediction": int(prediction[0])}
    
    except Exception as e:
        return {"message": f"Error during prediction: {str(e)}"}
