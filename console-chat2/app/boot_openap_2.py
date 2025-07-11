import os
import time
from app.common.app_constants import AppConstants, OpenAPIModelsEnum  , EmbeddingModelsEnum
from pathlib import Path
from app.common.helpers.DateFunctions import DateFunctions
from app.common.helpers.FileFunctions import FileFunctions
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever

print("✅ Usando langchain_openai (v0.3+)")

EMBEDDING_MODEL = EmbeddingModelsEnum.text_embedding_ada_002.value
TEMPERATURE = 0 #para test
OPENAI_MODEL = OpenAPIModelsEnum.gpt_3_5_turbo.value

ARCHIVO_LOG = Path(AppConstants.API_LOGS_PATH.value) / "processed_files.txt"
chat = ChatOpenAI(model=EMBEDDING_MODEL, temperature=0.7)

# https://chatgpt.com/c/686e721b-00d8-8002-aea9-7461e8cc375c
class ChatBootOpenApi2:
 def __init__(self):

        index_path = AppConstants.API_VECTOR_PATHH.value
       

        # self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.embedding_model = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=AppConstants.OPENAI_API_KEY.value
        )
        index_file = os.path.join(index_path, "index.faiss")
        
        # 3️⃣ Cargo el índice FAISS ya generado:
        if os.path.exists(index_file):
            self.vectorstore = FAISS.load_local(index_path, self.embedding_model, allow_dangerous_deserialization=True)
            # self.vectorstore = FAISS.load_local(directory=str(index_file), embeddings=self.embedding_model, allow_dangerous_deserialization=True)
            print("✅ Índice cargado correctamente.")
        else:
            print(f"⚠️ No se encontró el índice en {index_file}. Inicializando vectorstore vacío.")
            self.vectorstore = None  # o crear un FAISS nuevo si querés, con `FAISS.from_documents([], ...)`
       

        # 3. Instanciar el LLM
        self.llm = ChatOpenAI(
            model_name=OPENAI_MODEL,
            temperature=TEMPERATURE,
            openai_api_key=AppConstants.OPENAI_API_KEY.value
        )

        # 5.0 Defino el QA chain (“stuff”):
        # self.prompt = PromptTemplate.from_template("""
        # Sos el asistente interno de la empresa.
        # Usá este contexto para responder con claridad:

        # {context}

        # Pregunta: {question}
        # """)

        # 5.1 
        # Aquí usas un ChatPromptTemplate basado en mensajes, junto con un MessagesPlaceholder,
        # para reformular la entrada del usuario de modo que sea independiente del historial.
        # Esa consulta reformulada alimenta al retriever.
        contextualize_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Dada la siguiente conversación y una nueva pregunta, "
             "reformula la pregunta para que sea independiente del historial:\n\n"
             "{chat_history}\n\n"
             "Pregunta original: {input}\n\n"
             "Reformulación:"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        # 4️⃣ Creo el retriever conversacional:
        base_retriever = self.vectorstore.as_retriever(search_kwargs={"k":3})
         # 5. Cadena history-aware
        history_retriever = create_history_aware_retriever(
            self.llm,
            base_retriever,
            contextualize_prompt
        )
        # self.retriever = create_history_aware_retriever(base_ret)
        # 6. Prompt para generar la respuesta usando el contexto recuperado
        retrieval_qa_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Usa el siguiente contexto para responder la pregunta. "
             "Si no sabes la respuesta, di que no lo sabes.\n\n"
             "Contexto:\n{context}"),
            ("user", "{input}")
        ])
        # 7. Cadena para “stuff” de documentos
        stuff_chain = create_stuff_documents_chain(
            self.llm,
            retrieval_qa_prompt
        )
        # qa_chain = create_stuff_documents_chain(
        #     llm=ChatOpenAI(
        #         model=OPENAI_MODEL, 
        #         temperature=TEMPERATURE,
        #         openai_api_key=AppConstants.OPENAI_API_KEY.value
        # ),
        #     prompt=self.prompt
        # )

        # 6️⃣ Ensamblo el pipeline RAG -->  Pipeline RAG completo
        self.rag_chain = create_retrieval_chain(
            retriever=history_retriever,
            combine_docs_chain=stuff_chain
        )

 def run_chat(self):
    if not self.rag_chain:
        print("❌ No se pudo inicializar la cadena. No hay vectorstore.")
        return
                
    print("🤖 Chat type 'exit' to end.\n")
    chat_history = []
    while True:
        prompt = input("👤 Vos: ")
        if prompt.lower() in ["exit", "quit"]:
           print("🤖 End.")
           break
        try:
            result = self.rag_chain.invoke({
                    "input": prompt,
                    "chat_history": chat_history
                })
            answer = result["answer"]
            print(f"🤖 Walter bot: {answer}")
            chat_history.append((prompt, answer))

        except Exception as e:
            print(f"⚠️ Error atrapado: {e}")




