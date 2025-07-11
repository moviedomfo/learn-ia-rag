import os
from langchain_openai import ChatOpenAI
from openai import RateLimitError ,AuthenticationError,OpenAIError

from common.app_constants import AppConstants

def run_check():
    try:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                   temperature=0,
                   openai_api_key=AppConstants.OPENAI_API_KEY.value)    
        
        res = llm.invoke([{"role": "user", "content": "Di hola"}])
        print(res)

    except RateLimitError as e:
        print("🛑 Error: Superaste tu cuota de uso de OpenAI.")
        print("💡 Revisá tu plan o billing en https://platform.openai.com/account/usage")

    except AuthenticationError:
        print("🛑 Error de autenticación: Verificá que la API Key sea válida.")

    except OpenAIError as e:
        print(f"⚠️ Error inesperado de OpenAI: {e}")

    except Exception as e:
        print(f"❌ Error desconocido: {e}")


if __name__ == "__main__":
    run_check()