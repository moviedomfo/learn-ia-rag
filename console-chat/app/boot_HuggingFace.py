import os
import time
from app.common.app_constants import AppConstants  
from pathlib import Path

from app.common.helpers.DateFunctions import DateFunctions
from app.common.helpers.FileFunctions import FileFunctions
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

print("✅ Usando HuggingFaceEmbeddings")

ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"
def __init__(self, index_path="vector_index"):

        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = FAISS.load_local(index_path, self.embedding_model)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Podés usar modelos más chicos también, como "google/flan-t5-base"
        self.llm = HuggingFaceHub(
            repo_id="google/flan-t5-base",
            model_kwargs={"temperature": 0.5, "max_new_tokens": 256}
        )

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            memory=self.memory
        )
def start():
    print("💬 Chat IA iniciado. Escribí 'salir' para terminar.\n")

    while True:
        prompt = input("👤 Vos: ")
        if prompt.lower() == "salir":
            break

        response = chat.invoke([HumanMessage(content=prompt)])
        print(f"🤖 Walter bot: {response}")


def run_chat(self):
        print("🧠 IA cargada. Escribí tu pregunta (o 'salir' para terminar):")
        while True:
            pregunta = input("\n👤 Vos: ")
            if pregunta.lower() in ["salir", "exit", "quit"]:
                print("👋 Fin de la charla.")
                break

            response = self.chain.run(pregunta)
            print(f"🤖 IA: {response}")

    
