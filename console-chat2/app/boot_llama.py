import os
from pathlib import Path
# from langchain.llms import LlamaCpp
from langchain_community.llms import ollama
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.common.app_constants import AppConstants, EmbeddingModelsEnum
# from langchain.embeddings import SentenceTransformerEmbeddings
# from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = EmbeddingModelsEnum.all_MiniLM_L6_v2.value
TEMPERATURE = 0 #para test
LLAMA_MODEL = "llama2-7b.gguf"

ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"
# https://chatgpt.com/g/g-p-686fad31f90c8191a521997b85127ce3-ia/c/686fc184-9918-8002-8a63-2ea0176f4768
class ChatBootLlama:
 def __init__(self):
    index_path = AppConstants.API_VECTOR_PATHH.value

    # 1. Embeddings local
    self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # 2. Cargá (o reconstruí) tu FAISS index
    index_file = os.path.join(index_path, "index.faiss")
    
    # 3️⃣ Cargo el índice FAISS ya generado:
    if os.path.exists(index_file):
      self.vectorstore = FAISS.load_local(index_path, self.embedding_model, allow_dangerous_deserialization=True)
      print("✅ Índice cargado correctamente.")
    else:
      print(f"⚠️ No se encontró el índice en {index_file}. Inicializando vectorstore vacío.")
      self.vectorstore = None  # o crear un FAISS nuevo si querés, con `FAISS.from_documents([], ...)`
       

    # 3. Retriever base
    base_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    # 4. LLM local con llama-cpp
    llm = ollama(
        model_path=LLAMA_MODEL,
        n_threads=4,
        temperature=0.7
    )

    # 5. Prompt de reformulación con historial
    contextualize = ChatPromptTemplate.from_messages([
        ("system",
        "Dados estos intercambios y una pregunta nueva, reformulá la pregunta para que no dependa del historial:\n\n"
        "{chat_history}\n\n"
        "Pregunta: {input}\n\n"
        "Reformulación:"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    history_retriever = create_history_aware_retriever(
        llm,
        base_retriever,
        contextualize
    )

    # 6. Prompt para responder usando el contexto
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system",
        "Usá este contexto para responder. Si no sabés, respondé que no lo sabés.\n\n"
        "Contexto:\n{context}"),
        ("user", "{input}")
    ])

    stuff_chain = create_stuff_documents_chain(
        llm,
        qa_prompt
    )

    # 7. Pipeline RAG completo
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
        if pregunta.lower() in ["salir", "exit", "quit"]:
            print("🤖 Chau, éxito con tu proyecto.")
            break
        try:
            out = self.rag_chain.invoke({
                "input": pregunta,
                "chat_history": chat_history
            })
            respuesta = out["answer"]
            print(f"🤖 Bot local: {respuesta}")
            chat_history.append((pregunta, respuesta))
        except Exception as e:
            print(f"⚠️ Error: {e}")
