import os
from crewai.tools import tool
import joblib
import pandas as pd

from config.settings import Settings

# Load settings and model once at module level
settings = Settings()
model_path = os.getenv("MODEL_PATH")
model = joblib.load(model_path)


def predict_diabetes_core(patient_data: dict) -> dict:
    """
    Predict diabetes outcome for new patient data.

    Args:
        patient_data (dict): Dictionary with patient features:
            {
                "Pregnancies": int,
                "Glucose": float,
                "BloodPressure": float,
                "SkinThickness": float,
                "Insulin": float,
                "BMI": float,
                "DiabetesPedigreeFunction": float,
                "Age": int
            }

    Returns:
        dict: Prediction result with class, label, and probability.
    """
    df = pd.DataFrame([patient_data])
    pred_class = model.predict(df)[0]
    pred_prob = round(model.predict_proba(df)[0][1], 2)
    label = "Diabetic" if pred_class == 1 else "Non-Diabetic"
    return {
        "prediction": int(pred_class),
        "label": label,
        "probability_diabetic": float(pred_prob),
    }


@tool("Diabetes Prediction Tool")
def predict_diabetes(patient_data: dict) -> dict:
    """
    Predict diabetes outcome for new patient data.

    Args:
        patient_data (dict): Keys Pregnancies, Glucose, BloodPressure, SkinThickness,
            Insulin, BMI, DiabetesPedigreeFunction, Age.

    Returns:
        dict: prediction (0/1), label, probability_diabetic.
    """
    return predict_diabetes_core(patient_data)
