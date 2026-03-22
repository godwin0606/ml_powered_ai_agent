from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# load env variables
load_dotenv()

class Settings(BaseSettings):
    PERPLEXITY_API_KEY: str
    DEFAULT_LLM: str
    # BASE_URL: str
    DEFAULT_TEMPERATURE: str
    DATASET_PATH: str
    MODEL_PATH: str
    OTEL_SDK_DISABLED: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
