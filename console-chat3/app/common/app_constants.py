from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()  # Carga el .env por defecto desde el mismo directorio


class AppConstants(Enum):
    APP_PATH = os.getenv("APP_FILES_PATH")
    APP_URL  = os.getenv("API_URL")
    API_LOGS_PATH  = os.getenv("API_LOGS_PATH")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    API_VECTOR_PATHH = os.getenv("API_VECTOR_PATHH")
    HUGGINGFACEHUB_API_TOKEN  = os.getenv("HUGGINGFACEHUB_API_TOKEN")



class EmbeddingModelsEnum(Enum):
    text_embedding_ada_002 = "text-embedding-ada-002"
    all_MiniLM_L6_v2 = "all-MiniLM-L6-v2"
    

class OpenAPIModelsEnum(Enum):
    gpt_3_5_turbo = "gpt-3.5-turbo"
    gpt_4o="gpt-4o"
    gpt_4o_mini="gpt-4o-mini"
    text_davinci_003 = "text-davinci-003"

# https://huggingface.co/models
class HuggingFaceModelsEnum(Enum):
    google_flan_t5_base = "google/flan-t5-base"
    mistralai_Mistral_7B_Instruct_v01="mistralai/Mistral-7B-Instruct-v0.1"
    HuggingFaceTB_SmolLM3_3B = "HuggingFaceTB/SmolLM3-3B"
    deepseek_ai_DeepSeek_R1_0528_Qwen3_8B = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"
    

class LlamaModelsEnum(Enum):
    """
    Enum representing available Llama model variants.
    """

    #    llama3:latest - parameter_size: 8.0B, quantization_level: Q4_0
    llama3 = "llama3"
    """
     llama3:latest
       parameter_size: 8.0B
       quantization_level: Q4_0
    """
    llama3_2_1B_Q4_0 = "llama3.2:1B"
    """
     llama3.2:1b 
         parameter_size: 1.2B
         quantization_level: Q8_0
    """

from enum import Enum

class LogIcon(Enum):
    OK = "✅"
    WARN = "⚠️"
    ERROR = "🛑"
    INFO = "ℹ️"
    DEBUG = "🐞"
    SUCCESS = "🚀"
    BOOT = "🤖"