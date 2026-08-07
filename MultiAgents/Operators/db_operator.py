from dotenv import load_dotenv
import os
import chromadb
from chromadb.utils import embedding_functions

class DBOperator:
    def __init__(self):
        load_dotenv()

        self.client = chromadb.PersistentClient(os.getenv("DB_PATH"))
        self.embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=os.getenv("embedding_model")
        )
        self.collection = self.client.get_collection(
            name=os.getenv("nutrition_db_name"),
            embedding_function=self.embedder
        )

    def Query_DB(self, query: str) -> str:
        """
        Look up calorie information for a specific food item.

        Args:
            query: The food item to look up.

        Returns:
            A string containing nutrition information, or an empty string
            when no relevant results are found.
        """
        print(query)
        return
        results = self.collection.query(
            query_texts=[query],
            n_results=int(os.getenv("query_results_count", "5")),
            include=["documents", "metadatas", "distances"],
        )

        formatted_results = []
        threshold = float(os.getenv("threshold", "1.0"))

        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for metadata, distance in zip(metadatas, distances):
            if distance > threshold:
                continue

            print(metadata)
            print(distance)
            food_item = str(metadata.get("food_item", "Unknown")).title()
            calories = metadata.get("calories_per_100g", "Unknown")
            category = str(metadata.get("food_category", "Unknown")).title()

            formatted_results.append(
                f"{food_item} ({category}): {calories} calories per 100g"
            )

        if not formatted_results:
            return ""

        return "Nutrition Information:\n" + "\n".join(formatted_results)
