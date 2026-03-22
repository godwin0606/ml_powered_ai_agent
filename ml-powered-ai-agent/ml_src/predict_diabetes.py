import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
import pandas as pd

from config.settings import Settings

def predict_diabetes(new_data: dict) -> dict:
    """
    Predict diabetes outcome for new patient data.

    Args:
        new_data (dict): Dictionary with patient features:
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
    # Load model from settings
    settings = Settings()
    model_path = settings.MODEL_PATH
    model = joblib.load(model_path)

    # Convert dict → DataFrame (1 row)
    df = pd.DataFrame([new_data])

    # Predict
    pred_class = model.predict(df)[0]
    pred_prob = model.predict_proba(df)[0][1]

    # Add human-readable label
    label = "Diabetic" if pred_class == 1 else "Non-Diabetic"

    return {
        "prediction": int(pred_class),   # 0 = Non-diabetic, 1 = Diabetic
        "label": label,
        "probability_diabetic": float(pred_prob)
    }


if __name__ == "__main__":
    # Example patient 1 - Likely Diabetic
    patient_diabetic = {
        "Pregnancies": 3,
        "Glucose": 150,
        "BloodPressure": 80,
        "SkinThickness": 25,
        "Insulin": 100,
        "BMI": 30.5,
        "DiabetesPedigreeFunction": 0.6,
        "Age": 40
    }

    # Example patient 2 - Likely Non-Diabetic
    patient_non_diabetic = {
        "Pregnancies": 1,
        "Glucose": 95,
        "BloodPressure": 70,
        "SkinThickness": 20,
        "Insulin": 85,
        "BMI": 22.5,
        "DiabetesPedigreeFunction": 0.2,
        "Age": 25
    }

    result1 = predict_diabetes(patient_diabetic)
    result2 = predict_diabetes(patient_non_diabetic)

    print("✅ Prediction (Diabetic Case):", result1)
    print("✅ Prediction (Non-Diabetic Case):", result2)
