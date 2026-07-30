from dotenv import load_dotenv
import os
import chromadb
from chromadb.utils import embedding_functions

class DBOperator:
    def __init__(self):
        load_dotenv()

        self.client = chromadb.PersistentClient(os.getenv("DB_PATH"))
        self.embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=os.getenv("EMBEDDING_MODEL")
        )
        self.collection = self.client.get_collection(
            name=os.getenv("NUTRITION_DB_NAME"),
            embedding_function=self.embedder
        )
