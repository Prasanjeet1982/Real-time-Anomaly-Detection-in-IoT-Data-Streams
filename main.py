import numpy as np
from fastapi import FastAPI
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

app = FastAPI()

# Initialize preprocessing steps and Isolation Forest
preprocessor = StandardScaler()
clf = IsolationForest()

# Create a pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('clf', clf)
])

# Define parameter grid for hyperparameter tuning
param_grid = {
    'clf__n_estimators': [50, 100, 200],
    'clf__contamination': [0.01, 0.05, 0.1]
}

# Initialize GridSearchCV for model optimization
grid_search = GridSearchCV(pipeline, param_grid, scoring='neg_mean_squared_error', cv=3)

@app.post("/detect-anomalies/")
async def detect_anomalies(data: np.ndarray):
    """
    Detect anomalies in a stream of IoT data.

    Parameters:
    - data (np.ndarray): 2D array of data points where each row represents a data point.

    Returns:
    - dict: Dictionary containing the indices of detected anomalies.
    """
    # Fit and predict using the GridSearchCV object
    grid_search.fit(data)
    predictions = grid_search.best_estimator_.predict(data)
    
    anomaly_indices = [i for i, prediction in enumerate(predictions) if prediction == -1]
    
    return {"anomaly_indices": anomaly_indices}

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
