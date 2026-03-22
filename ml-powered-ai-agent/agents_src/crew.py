from crewai import Crew
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents_src.agents.diabetes_prediction_agent import diabetes_prediction_agent
from agents_src.tasks.diabetes_prediction_task import predict_diabetes_task

diabetes_prediction_crew = Crew(
    agents=[diabetes_prediction_agent],
    tasks=[predict_diabetes_task],
    verbose=True
)
