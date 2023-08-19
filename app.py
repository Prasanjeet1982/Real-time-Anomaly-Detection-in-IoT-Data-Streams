# app.py

import numpy as np
import joblib
from fastapi import FastAPI
from model import train_model

app = FastAPI()

# Load the trained model
best_model = joblib.load('anomaly_detection_model.pkl')

@app.post("/detect-anomalies/")
async def detect_anomalies(data: np.ndarray):
    predictions = best_model.predict(data)
    anomaly_indices = [i for i, prediction in enumerate(predictions) if prediction == -1]
    return {"anomaly_indices": anomaly_indices}
