from pydantic import BaseModel
from typing import List, Any
from crewai import Task
from agents_src.agents.diabetes_prediction_agent import diabetes_prediction_agent


class DiabetesRiskPrediction(BaseModel):
    result: str  # 'Positive' or 'Negative'
    probability_diabetic: float
    test_result_natural_language: str  # Human-readable summary of the test result

class DiabetesPredictionOutput(BaseModel):
    diabetes_risk_prediction: DiabetesRiskPrediction
    explanation: List[str]
    actionable_health_advice: List[str]
    tool_output: Any


predict_diabetes_task = Task(
    description=(
        "The diabetes model has already been run; you do not have tools. Use only this output.\n"
        "prediction_result (authoritative): {prediction_result}\n"
        "patient_data (for context): {patient_data}\n"
        "Summarize the prediction clearly and give actionable health advice tailored to the result. "
        "Set tool_output to the same dict as prediction_result (the raw model output)."
    ),
    expected_output=(
        "A Python dict with the following structure: "
        "{'diabetes_risk_prediction': {'result': <'Positive' or 'Negative'>, 'probability': <float>, 'test_result_natural_language': <str>}, "
        "'explanation': [<bullet-pointed explanations>], "
        "'actionable_health_advice': [<bullet-pointed recommendations>], "
        "'tool_output': <raw output from the diabetes prediction tool>}"
        "\nThe 'test_result_natural_language' field should provide a human-readable summary of the test result."
    ),
    output_pydantic=DiabetesPredictionOutput,
    agent=diabetes_prediction_agent
)
