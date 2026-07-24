import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
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

    def query_db(self, query:str):
        results = self.collection.query(
            query_texts=[query],
            n_results=int(os.getenv("QUERY_RESULTS_COUNT")),
        )

        formatted_results = []

        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i]
            food_item = metadata["food_item"].title()
            calories = metadata["calories_per_100g"]
            category = metadata["food_category"].title()

            formatted_results.append(
                f"{food_item} ({category}): {calories} calories per 100g"
            )

            return "Nutrition Information:\n" + "\n".join(formatted_results)


