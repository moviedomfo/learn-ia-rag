import os
from langchain.document_loaders import TextLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# all-MiniLM-L6-v2
model ="paraphrase-multilingual-MiniLM-L12-v2"

class EmbeddingGeneratorOpenApi:
    def __init__(self, model_name=model):
        # Optionally accept a model for embedding generation
        self.model = model_name
        self.embedding_model = SentenceTransformerEmbeddings(model_name=model_name)


    def generate_embeddings(self, fulFileName:str):
   
        loader  = TextLoader(fulFileName)
        docs = loader.load()  # Devuelve una lista de Document(s)

        # 3. Dividir en chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        # 4. Crear embeddings con SentenceTransformers
        embedding_model = SentenceTransformerEmbeddings(model_name=model)
        vectorstore = FAISS.from_documents(chunks, embedding_model)

        return vectorstore
    
    def save_embeddings(self, index_path:str, vectorstore):
        # Chequear si existe índice anterior
        if os.path.exists(index_path):
            print("📂 Cargando índice existente...")
            existing_vector = FAISS.load_local(index_path, self.embedding_model,allow_dangerous_deserialization=True)
            existing_vector.merge_from(vectorstore)
            vectorstore = existing_vector
            print("🔗 Índice mergeado con documentos previos.")
      
         # Guardar el índice (nuevo o actualizado)
        vectorstore.save_local(index_path)
        print("💾 Índice guardado en disco.")

   