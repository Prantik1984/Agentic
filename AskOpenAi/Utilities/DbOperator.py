import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

class DBOperator:
    def __init__(self):
        load_dotenv()
    def extract_nutrition_data(self,db_path:str,file_path:str):
        df = pd.read_csv(file_path)
        documents = []
        metadatas = []
        ids = []
        for index, row in df.iterrows():
            cals = str(row['Cals_per100grams']).replace(' cal', '')
            kj = str(row['KJ_per100grams']).replace(' kJ', '')

            document_text = f"""
                   FoodName: {row["FoodItem"]}
                   Nutritional Information:
                   - Calories: {cals} per 100g
                   - Energy: {kj} kJ per 100g
                   - Serving size reference: {row['per100grams']}
                   This is a {row['FoodCategory'].lower()} food item that provides {cals} calories per 100 grams.
                   """
            documents.append(document_text)

            metadata = {
                "food_item": row["FoodItem"].lower(),
                "food_category": row["FoodCategory"].lower(),
                "calories_per_100g": (
                    cals
                ),
                "kj_per_100g": (
                    kj
                ),
                "serving_info": row["per100grams"],
                # Add searchable keywords
                "keywords": f"{row['FoodItem'].lower()} {row['FoodCategory'].lower()}".replace(
                    " ", "_"
                ),
            }

            metadatas.append(metadata)
            ids.append(f"food_{index}")

        return documents, metadatas, ids

    def Create_CSV_DB(self,db_path:str,file_path:str):
        documents, metadatas, ids = self.extract_nutrition_data(db_path,file_path)
        client = chromadb.PersistentClient(path=db_path)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=os.getenv("embedding_model")
        )
        collection = client.get_or_create_collection(
            name=os.getenv("nutrition_db_name"),
            embedding_function=embedder,
            metadata={"hnsw:space": "cosine"}
        )
        collection.add(ids=ids, documents=documents,metadatas=metadatas)


    def Query_CSV_DB(self,query:str,db_path:str):
        """
            Tool function for a RAG database to look up calorie information for specific food items, but not for meals.

            Args:
                query: The food item to look up.
                db_path:The path of the RAG database.
            Returns:
                A string containing the nutrition information.
            """
        client = chromadb.PersistentClient(path=db_path)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=os.getenv("embedding_model")

        )
        collection = client.get_collection(
            name=os.getenv("nutrition_db_name"),
            embedding_function=embedder
        )
        results = collection.query(
            query_texts=[query],
            n_results=int(os.getenv("query_results_count")),
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

