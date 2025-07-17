from langchain_ollama  import OllamaLLM
from langchain_core.language_models.llms import LLM
from common.app_constants import LlamaModelsEnum
from common.app_constants import AppConstants

def run_check():
    try:
        llm :OllamaLLM = OllamaLLM(
            model=LlamaModelsEnum.llama3_2_1B_Q4_0,
            temperature=0)

        # llm = ChatOpenAI(model_name="gpt-3.5-turbo",
        #            temperature=0,
        #            openai_api_key=AppConstants.OPENAI_API_KEY.value)    
        
        res = llm.invoke([{"role": "user", "content": "Di hola"}])
        print(res)

  
    except Exception as e:
        print(f"❌ Error desconocido: {e}")

if __name__ == "__main__":
    run_check()