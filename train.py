# train.py

import joblib
from data_loader import load_data
from model import train_model

historical_data = load_data()
best_model = train_model(historical_data)

# Save the trained model to a file
joblib.dump(best_model, 'anomaly_detection_model.pkl')

print("Model training completed and saved as 'anomaly_detection_model.pkl'.")
