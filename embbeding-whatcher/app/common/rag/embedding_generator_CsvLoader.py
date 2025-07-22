import os
from langchain.document_loaders import CSVLoader
# from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


#model = "intfloat/multilingual-e5-large"
model ="paraphrase-multilingual-MiniLM-L12-v2"
chunk_size: int = 400
chunk_overlap: int = 50


class EmbeddingGeneratorCSVLoader:
    """Generates embeddings from a CSV file using HuggingFace embeddings.
       docs: https://python.langchain.com/api_reference/huggingface/embeddings/langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings.html
    """
    def __init__(self, model_name=model):
        self.model = model_name
        # self.embedding_model = SentenceTransformerEmbeddings(model_name=model_name)
        
        # https://sbert.net/docs/package_reference/SentenceTransformer.html#sentence_transformers.SentenceTransformer.encode
        encode_kwargs={"normalize_embeddings": False}
        # model_kwargs :device, prompts, default_prompt_name, revision, trust_remote_code, or token. See also the Sentence Transformer documentation
        # https://sbert.net/docs/package_reference/SentenceTransformer.html#sentence_transformers.SentenceTransformer
        model_kwargs = {'device': 'cpu'} # p.ej. {"device": "cuda"}
        # cache_folder Path to store models. 
        
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,             
            encode_kwargs=encode_kwargs,
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )


    def generate_embeddings(self, fulFileName:str):
   
        # loader  = CSVLoader(fulFileName)
        # docs = loader.load()  # Devuelve una lista de Document(s)
        """Carga un CSV de facturas (una fila = una factura) y devuelve un vectorstore en memoria."""
        docs = CSVLoader(
            file_path=fulFileName,
            # Cada fila se convierte en Document(metadata={'row': i, ...})
            csv_args={"delimiter": ",", "quotechar": '"'},
        ).load()
        # 3. Dividir en chunks
        chunks = self.splitter.split_documents(docs)

        # 4. Crear embeddings con SentenceTransformers
        # self.embedding_model = SentenceTransformerEmbeddings(model_name=model)
        vectorstore = FAISS.from_documents(chunks, self.embedding_model)

        return vectorstore
    
    def save_embeddings(self, index_path:str, vectorstore):
        index_file = os.path.join(index_path, "index.faiss")

        # Chequear si existe índice anterior
        if os.path.exists(index_file):
            print("📂 Cargando índice existente...")
            existing_vector = FAISS.load_local(index_path, self.embedding_model,allow_dangerous_deserialization=True)
            existing_vector.merge_from(vectorstore)
            vectorstore = existing_vector
            print("🔗 Índice mergeado con documentos previos.")
      
         # Guardar el índice (nuevo o actualizado)
        vectorstore.save_local(index_path)
        print("💾 Índice guardado en disco.")

   