# https://chatgpt.com/g/g-p-686fad31f90c8191a521997b85127ce3-ia/c/686fc184-9918-8002-8a63-2ea0176f4768
# https://chatgpt.com/c/68795009-e0e8-8002-924a-5065ebc7a7cd

import os
from pathlib import Path
from app.common.app_constants import LlamaModelsEnum
from app.common.helpers.LogFunctions import LogFunctions
from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, AIMessage
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.common.app_constants import AppConstants, EmbeddingModelsEnum, LogIcon
from langchain_ollama  import OllamaLLM
# from langchain_community.embeddings import HuggingFaceEmbeddings #  deprecado
from langchain_huggingface import HuggingFaceEmbeddings
from app.common.Session.SessionState import SessionState


CHAT_CEL_NUMBER = '351-153398748'
EMBEDDING_MODEL = EmbeddingModelsEnum.all_MiniLM_L6_v2.value
TEMPERATURE = 0 #para test
LLAMA_MODEL = LlamaModelsEnum.llama3.value
ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"
asistente= "casandra"

class ChatBootLlama2:
    def __init__(self):
        # al inicio
        self.chat_history: list[BaseMessage] = []

        # 1. Embedding model
        self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

        # 2. Cargar FAISS index existente
        index_path = AppConstants.API_VECTOR_PATHH.value
        index_file = os.path.join(index_path, "index.faiss")

        if os.path.exists(index_file):
            self.vectorstore = FAISS.load_local(
                index_path,
                self.embedding_model,
                allow_dangerous_deserialization=True
            )
            LogFunctions.print_OK("Índice FAISS cargado.")
        else:
            LogFunctions.print_error(f"No se encontró el índice en {index_file}.")
            self.vectorstore = None

        base_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        # base_retriever = self.vectorstore.as_retriever(
        #     search_kwargs={"k": 3, "filter": {"SOCIO_NRO": self.socio_id}}
        #     )
        # 4. LLM local con llama-cpp
        self.llm:OllamaLLM  = OllamaLLM(model=LLAMA_MODEL,temperature=TEMPERATURE)
        
        # 5. Prompt de reformulación contextual
        contextualize = ChatPromptTemplate.from_messages([
            ("system",
             "Eres un asistente de la Cooperativa. "
             "Dado este historial de conversación y una nueva pregunta, reformulá la pregunta para que sea autocontenida:\n"
             "Reglas:\n- Un socio puede tener uno o más abonados.\n"
              "Si la pregunta sobre facturas es ambigua, pregunta si quiere el total "
              "de todos los abonados o uno específico.\n\n"
              "- Cada abonado emite una factura por período.\n\n"
              "- si ya tiene ubicado el cosio puedes saludorlo por su nombre.\n\n"
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
             "Reglas:\n- Un socio puede tener uno o más abonados.\n"
              "Si la pregunta sobre facturas es ambigua, pregunta si quiere el total "
              "de todos los abonados o uno específico.\n\n"
              "- Cada abonado emite una factura por período.\n\n"
              "- si ya tiene ubicado el cosio puedes saludorlo por su nombre.\n\n"
             "Contexto:\n{context}"),
            ("human", "{input}")
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
        LogFunctions.print_OK(" Chat local iniciado. escribí 'salir' para terminar.")
        state = SessionState(CHAT_CEL_NUMBER)
        s = state.has_socio(CHAT_CEL_NUMBER)

        # Si no hay datos del socio, pedirlos y persistirlos
        if s.nro_abonado is None:   
            LogFunctions.print_error("No se encontró el socio asociado al número de teléfono.")
            nro_socio = input("Ingresa el Nro de socio: ")
            state.socio.nro_socio = nro_socio
            nro_abonado = input("Ingresa el Nro de abonado: ")
            state.socio.nro_abonado = nro_abonado
            state.socio.nombre = input("Ingresa el nombre del socio: ")
            state.persist_socio()
            # Actualizar s después de guardar
            s = state.has_socio(CHAT_CEL_NUMBER)

        # Agregar información relevante del socio al chat_history como contexto inicial
        socio_context = (
            f"Datos del socio:\n"
            f"- Nombre: {s.nombre}\n"
            f"- Nro de socio: {s.nro_socio}\n"
            f"- Nro de abonado: {s.nro_abonado}\n"
        )
        self.chat_history = [
            HumanMessage(content="Estos son mis datos personales para futuras consultas."),
            AIMessage(content=socio_context)
        ]

        LogFunctions.print_BOOT(f"Hola soy {asistente} {s.nombre}, ¿en qué puedo ayudarte hoy?")

        while True:
            pregunta = input(f"👤{s.nombre}: ")
            if pregunta.lower() in ["q", "exit", "quit", "salir"]:
                LogFunctions.print_BOOT("Chau, éxito con tu proyecto.")
                break
            try:
                self.chat_history.append(HumanMessage(content=pregunta))
                out = self.rag_chain.invoke({
                    "input": pregunta,
                    "chat_history": self.chat_history
                })
                respuesta = out["answer"]
                LogFunctions.print_BOOT({respuesta})
                self.chat_history.append(AIMessage(content=respuesta))
            except Exception as e:
                LogFunctions.print_error(f"Error: {e}")

