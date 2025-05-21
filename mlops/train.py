import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os
from datetime import datetime

def load_data():
    # TODO: Implement data loading from your code review dataset
    # This is a placeholder implementation
    return pd.DataFrame({
        'code': ['sample code 1', 'sample code 2'],
        'quality_score': [0.8, 0.6],
        'has_bugs': [0, 1]
    })

def train_model(X_train, y_train):
    # TODO: Implement your model training logic
    # This is a placeholder implementation
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    return {
        'accuracy': accuracy_score(y_test, predictions),
        'precision': precision_score(y_test, predictions),
        'recall': recall_score(y_test, predictions),
        'f1': f1_score(y_test, predictions)
    }

def main():
    # Set up MLflow
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("code_review_model")

    # Load and prepare data
    data = load_data()
    X = data[['code']]  # Add your feature engineering here
    y = data['has_bugs']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    with mlflow.start_run():
        # Train model
        model = train_model(X_train, y_train)

        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test)

        # Log parameters
        mlflow.log_params({
            'model_type': 'RandomForest',
            'test_size': 0.2
        })

        # Log metrics
        mlflow.log_metrics(metrics)

        # Log model
        mlflow.sklearn.log_model(model, "model")

        # Log additional artifacts
        with open("model_info.txt", "w") as f:
            f.write(f"Model trained at: {datetime.now()}\n")
            f.write(f"Metrics: {metrics}\n")
        mlflow.log_artifact("model_info.txt")

if __name__ == "__main__":
    main() 