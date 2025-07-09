import os
import time
from app.common.app_constants import AppConstants  
from pathlib import Path
from app.common.helpers.DateFunctions import DateFunctions
from app.common.helpers.FileFunctions import FileFunctions
# from langchain_community.vectorstores import FAISS
# from langchain_community.llms import HuggingFaceHub
# from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"
# model ="paraphrase-multilingual-MiniLM-L12-v2"
model = "all-MiniLM-L6-v2"
repo_id = "google/flan-t5-base"
class LocalVectorChat:

    def __init__(self):

        index_path = AppConstants.API_VECTOR_PATHH.value
        self.embedding_model = HuggingFaceEmbeddings(model_name=model)
        index_file = os.path.join(index_path, "index.faiss")

        if os.path.exists(index_file):
            self.vectorstore = FAISS.load_local(index_path, self.embedding_model, allow_dangerous_deserialization=True)
            print("✅ Índice cargado correctamente.")
        else:
            print(f"⚠️ No se encontró el índice en {index_file}. Inicializando vectorstore vacío.")
            self.vectorstore = None  # o crear un FAISS nuevo si querés, con `FAISS.from_documents([], ...)`
        

          # Podés usar modelos más chicos también, como "google/flan-t5-base"
        self.llm = HuggingFaceHub(
                repo_id=repo_id,
                 model_kwargs={"temperature": 0.5, "max_new_tokens": 512},
        huggingfacehub_api_token=AppConstants.HUGGINGFACEHUB_API_TOKEN

            )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        
        retriever_prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder("chat_history"),
            ("human", "{context}"),
            ("system", "Respondé basándote solo en los documentos si es posible."),
        ])
        
        self.history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, retriever_prompt
        )

        chain_prompt = ChatPromptTemplate.from_messages([
            ("system", "Respondé con claridad y precisión."),
            MessagesPlaceholder("chat_history"),
            ("human", "{context}"),
        ])

        combine_docs_chain = create_stuff_documents_chain(llm=self.llm,prompt=chain_prompt)

        self.chain = create_retrieval_chain(
            retriever=self.history_aware_retriever,
            combine_docs_chain=combine_docs_chain
        )

        # self.chain = create_retrieval_chain(
        #     retriever=self.history_aware_retriever,
        #     combine_docs_chain=self.llm,
        #     prompt=chain_prompt
        # )
        # Estado de la conversación
        self.chat_history = []
        # self.chain = ConversationalRetrievalChain.from_llm(
        #         llm=self.llm,
        #         retriever=retriever,
        #         memory=self.memory
        #     )


    def run_chat(self):
            if not self.chain:
                print("❌ No se pudo inicializar la cadena. No hay vectorstore.")
                return
            
            print("🧠 IA cargada. Escribí tu pregunta (o 'salir' para terminar):")
            while True:
                pregunta = input("\n👤 Vos: ")
                if pregunta.lower() in ["salir", "exit", "quit"]:
                    print("👋 Fin de la charla.")
                    break

                try:
                    inputs = {"input": pregunta, "chat_history": self.chat_history}
                    response = self.chain.invoke(inputs)
                    print(f"🤖 IA: {response}")

                    # Guardamos la conversación
                    self.chat_history.append(HumanMessage(content=pregunta))
                    self.chat_history.append(AIMessage(content=response.content))
                except Exception as e:
                    print(f"⚠️ Error atrapado: {e}")

        
