import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.utils import shuffle

from config.settings import Settings

def train_diabetes_model(dataset_path, model_path):

    # -------------------------------
    # 1. Load Dataset
    # -------------------------------
    df = pd.read_csv(dataset_path)

    # -------------------------------
    # 2. Data Cleaning
    # -------------------------------
    cols_with_zeros = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    df[cols_with_zeros] = df[cols_with_zeros].replace(0, np.nan)
    df.fillna(df.median(), inplace=True)

    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]

    # -------------------------------
    # 3. Train-Test Split
    # -------------------------------
    X, y = shuffle(X, y, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # -------------------------------
    # 4. Hyperparameter Grid
    # -------------------------------
    param_dist = {
        "n_estimators": [100, 200, 300, 400, 500],
        "max_depth": [3, 5, 7, 10, None],
        "min_samples_split": [2, 5, 10, 15],
        "min_samples_leaf": [1, 2, 5, 10],
        "max_features": ["sqrt", "log2", None],
        "class_weight": ["balanced"]
    }

    rf = RandomForestClassifier(random_state=42)

    random_search = RandomizedSearchCV(
        estimator=rf,
        param_distributions=param_dist,
        n_iter=30,
        cv=5,
        scoring="accuracy",
        verbose=1,
        random_state=42,
        n_jobs=-1
    )

    # -------------------------------
    # 5. Train Best Model
    # -------------------------------
    random_search.fit(X_train, y_train)
    best_model = random_search.best_estimator_

    print("\n✅ Best Hyperparameters:")
    print(random_search.best_params_)

    # -------------------------------
    # 6. Evaluation
    # -------------------------------
    y_train_pred = best_model.predict(X_train)
    y_test_pred = best_model.predict(X_test)

    print("\n📊 Model Performance:")
    print(f"Training Accuracy: {accuracy_score(y_train, y_train_pred):.4f}")
    print(f"Test Accuracy: {accuracy_score(y_test, y_test_pred):.4f}")
    print("ROC-AUC:", roc_auc_score(y_test, best_model.predict_proba(X_test)[:,1]))

    print("\nClassification Report (Test Data):")
    print(classification_report(y_test, y_test_pred))

    # -------------------------------
    # 7. Save Model
    # -------------------------------
    joblib.dump(best_model, model_path)
    print(f"\n💾 Model saved to {model_path}")

    return best_model

if __name__ == "__main__":
    settings = Settings()
    DATASET_PATH = settings.DATASET_PATH
    MODEL_PATH = settings.MODEL_PATH
    train_diabetes_model(DATASET_PATH, MODEL_PATH)
