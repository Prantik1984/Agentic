import os
from pathlib import Path
import csv
import re
from Vectorizers.text_embeder import TextEmbedder

class CSVRetriever:
    def __init__(self,embedding_model):
        self.text_embedder = TextEmbedder(embedding_model)

    def num(self,s:str):
        m = re.search(r"-?\d+(?:\.\d+)?", s or '')
        return float(m.group()) if m else 0.0

    def getdata(self,csv_file:str):
        """"
        reads the csv file and returns the docs and metadatas that
        need to be upserted to the chromadb
        """
        if not os.path.exists(csv_file):
            print(f"File {csv_file} does not exist")
            return None

        ids, docs, metas, embs = [], [], [], []
        csv_path= Path(csv_file)

        with csv_path.open(newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for i, r in enumerate(reader):
                category = (r.get('FoodCategory') or '').strip()
                item = (r.get('FoodItem') or '').strip()
                per = (r.get('per100grams') or '').strip()
                cals_raw = (r.get('Cals_per100grams') or '').strip()
                kj_raw = (r.get('KJ_per100grams') or '').strip()

                doc = f"{item}. Category: {category}. Nutrition per {per}: {cals_raw}, {kj_raw}."
                docs.append(doc)
                ids.append(f"food_{i:05d}")
                metas.append({
                    "row": i,
                    "food_category": category,
                    "food_item": item,
                    "per_100_grams": per,
                    "calories_per_100g": self.num(cals_raw),
                    "kj_per_100g": self.num(kj_raw),
                    "calories_raw": cals_raw,
                    "kj_raw": kj_raw,
                })
                embs.append(self.text_embedder.embed_text(doc))

        return ids, docs, metas, embs





