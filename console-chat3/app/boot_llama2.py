import os
from pathlib import Path
# from langchain_community.llms import ollama
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.common.app_constants import AppConstants, EmbeddingModelsEnum
from langchain_ollama  import OllamaLLM
# from langchain_core.language_models.llms import LLM
from app.common.app_constants import LlamaModelsEnum
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBEDDING_MODEL = EmbeddingModelsEnum.all_MiniLM_L6_v2.value
TEMPERATURE = 0 #para test
LLAMA_MODEL = "llama2-7b.gguf"
ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"
# https://chatgpt.com/g/g-p-686fad31f90c8191a521997b85127ce3-ia/c/686fc184-9918-8002-8a63-2ea0176f4768

class ChatBootLlama2:
    def __init__(self):
        # 1. Embedding model
        embedding_model_name = EmbeddingModelsEnum.all_MiniLM_L6_v2.value
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)

        # 2. Cargar FAISS index existente
        index_path = AppConstants.API_VECTOR_PATHH.value
        index_file = os.path.join(index_path, "index.faiss")

        if os.path.exists(index_file):
            self.vectorstore = FAISS.load_local(
                index_path,
                self.embedding_model,
                allow_dangerous_deserialization=True
            )
            print("✅ Índice FAISS cargado.")
        else:
            print(f"⚠️ No se encontró el índice en {index_file}.")
            self.vectorstore = None

        base_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        # 4. LLM local con llama-cpp
        self.llm:OllamaLLM  = OllamaLLM(model=LlamaModelsEnum.llama3_2_1B_Q4_0.value)
        print(f"model={LlamaModelsEnum.llama3_2_1B_Q4_0.value}")
        
        # 5. Prompt de reformulación contextual
        contextualize = ChatPromptTemplate.from_messages([
            ("system",
             "Dado este historial de conversación y una nueva pregunta, reformulá la pregunta para que sea autocontenida:\n"
             "{chat_history}\n\n"
             "Nueva pregunta: {input}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        # 6. Retriever que tiene en cuenta el historial
        history_retriever = create_history_aware_retriever(
            self.llm,
            base_retriever,
            contextualize
        )

        # 7. Prompt para responder con contexto
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Usá el siguiente contexto para responder. Si no sabés, decí que no lo sabés.\n\n"
             "Contexto:\n{context}"),
            ("user", "{input}")
        ])

        # 8. Stuff chain
        stuff_chain = create_stuff_documents_chain(
            self.llm,
            qa_prompt
        )

        # 9. RAG final
        self.rag_chain = create_retrieval_chain(
            history_retriever,
            stuff_chain
        )


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

