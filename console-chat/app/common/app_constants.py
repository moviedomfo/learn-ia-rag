from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()  # Carga el .env por defecto desde el mismo directorio


class AppConstants(Enum):
    APP_PATH = os.getenv("APP_FILES_PATH")
    APP_URL  = os.getenv("API_URL")
    API_LOGS_PATH  = os.getenv("API_LOGS_PATH")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



