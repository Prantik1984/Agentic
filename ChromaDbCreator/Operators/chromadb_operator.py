import chromadb

class ChromaDbOperator:
    def createdb(self,ids, docs, metas, embs,batch,db_path,
                 collection_name):
        """"
        Creates the chroma db
        """
        client = chromadb.PersistentClient(path=str(db_path))

        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

        collection = client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine", "source": "calories.csv"},
        )

        for start in range(0, len(ids), batch):
            end = start + batch
            collection.add(
                ids=ids[start:end], documents=docs[start:end],
                metadatas=metas[start:end], embeddings=embs[start:end]
            )
