import os
import time
from app.common.app_constants import AppConstants  
from pathlib import Path
from app.common.helpers.DateFunctions import DateFunctions
from app.common.helpers.FileFunctions import FileFunctions
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever

print("✅ Usando langchain_openai (v0.2.0+)")

# gpt-3.5-turbo
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TEMPERATURE = 0.2
OPENAI_MODEL = "gpt-3.5-turbo"

ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"
chat = ChatOpenAI(model=EMBEDDING_MODEL, temperature=0.7)

# https://chatgpt.com/c/686e721b-00d8-8002-aea9-7461e8cc375c
class ChatBootOpenApi:
 def __init__(self):

        index_path = AppConstants.API_VECTOR_PATHH.value
        self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        index_file = os.path.join(index_path, "index.faiss")
        
        # 3️⃣ Cargo el índice FAISS ya generado:
        if os.path.exists(index_file):
            # self.vectorstore = FAISS.load_local(index_path, self.embedding_model, allow_dangerous_deserialization=True)
            self.vectorstore = FAISS.load_local(directory=str(index_path), embeddings=self.embedding_model, allow_dangerous_deserialization=True)
            print("✅ Índice cargado correctamente.")
        else:
            print(f"⚠️ No se encontró el índice en {index_file}. Inicializando vectorstore vacío.")
            self.vectorstore = None  # o crear un FAISS nuevo si querés, con `FAISS.from_documents([], ...)`
       
        # 5️⃣ Defino el QA chain (“stuff”):
        self.prompt = PromptTemplate.from_template("""
        Sos el asistente interno de la empresa.
        Usá este contexto para responder con claridad:

        {context}

        Pregunta: {question}
        """)

        # 4️⃣ Creo el retriever conversacional:
        base_ret = self.vectorstore.as_retriever(search_kwargs={"k":3})
        self.retriever = create_history_aware_retriever(base_ret)

        qa_chain = create_stuff_documents_chain(
            llm=ChatOpenAI(
                model=OPENAI_MODEL, 
                temperature=TEMPERATURE,
                openai_api_key=AppConstants.OPENAI_API_KEY.value
        ),
            prompt=self.prompt
        )

        # 6️⃣ Ensamblo el pipeline RAG:
        self.rag_chain = create_retrieval_chain(
            retriever=self.retriever,
            combine_docs_chain=qa_chain
        )

 def run_chat(self):
    if not self.rag_chain:
        print("❌ No se pudo inicializar la cadena. No hay vectorstore.")
        return
                
    print("🤖 Chat IA iniciado. Escribí 'salir' para terminar.\n")
    chat_history = []
    while True:
        prompt = input("👤 Vos: ")
        if prompt.lower() in ["salir", "exit", "quit"]:
           print("🤖 Fin de la charla.")
           break
        try:
        #    response = chat.invoke([HumanMessage(content=prompt)])
           out = self.rag_chain({"question": prompt, "chat_history": chat_history})
           response = out["answer"]
           print(f"🤖 Walter bot: {response}")
           chat_history.append((prompt, response  ))

        except Exception as e:
            print(f"⚠️ Error atrapado: {e}")




