import os
import sys
from crewai import Agent, LLM

from config.settings import Settings

settings = Settings()
model = os.getenv("DEFAULT_LLM")  
base_url = os.getenv("BASE_URL")
temperature = float(os.getenv("DEFAULT_TEMPERATURE", 0.0))

# initialize the llm
llm = LLM(
    model=model,
    # base_url = base_url,
    temperature=temperature
)

diabetes_prediction_agent = Agent(
    role="Diabetes Prediction Specialist",
    goal=(
        "Explain diabetes risk using the provided model output only (no tools), strictly from that data."
        " Provide clear, actionable health advice tailored to the prediction."
    ),
    backstory=(
        "You are an analytical yet supportive assistant. A deterministic model has already produced "
        "the risk scores; you interpret them accurately and offer practical recommendations. "
        "You never invent different numbers than the given prediction_result."
    ),
    llm=llm,
    verbose=True,
)
