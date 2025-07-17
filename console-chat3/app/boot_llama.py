import os
from pathlib import Path
# from langchain.llms import LlamaCpp
# from langchain_community.llms import ollama
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.common.app_constants import AppConstants, EmbeddingModelsEnum
from langchain_ollama  import OllamaLLM
from langchain_core.language_models.llms import LLM
from app.common.app_constants import LlamaModelsEnum

EMBEDDING_MODEL = EmbeddingModelsEnum.all_MiniLM_L6_v2.value
TEMPERATURE = 0 #para test
LLAMA_MODEL = "llama2-7b.gguf"
ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"
# https://chatgpt.com/g/g-p-686fad31f90c8191a521997b85127ce3-ia/c/686fc184-9918-8002-8a63-2ea0176f4768

class ChatBootLlama:
    def __init__(self):
      # 4. LLM local con llama-cpp
        self.llm:OllamaLLM  = OllamaLLM(model=LlamaModelsEnum.llama3_2_1B_Q4_0.value)
        print(f"model={LlamaModelsEnum.llama3_2_1B_Q4_0.value}")

# 8. Loop interactivo
    def run_chat(self):
        print("🤖 Chat local iniciado. escribí 'salir' para terminar.")
        chat_history = []
        while True:
            pregunta = input("👤 Vos: ")
            if pregunta.lower() in ["q", "exit", "quit"]:
                print("🤖 Chau, éxito con tu proyecto.")
                break
            try:
                
                # out = self.llm.invoke({
                #     "input": pregunta,
                #     "chat_history": chat_history
                # })
                respuesta = self.llm.invoke(pregunta)
                # respuesta = out["answer"]
                print(f"🤖 Bot local: {respuesta}")
                chat_history.append((pregunta, respuesta))
            except Exception as e:
                print(f"⚠️ Error: {e}")

