import sys
from DataRetrievers.csv_retriever import CSVRetriever
from Operators.chromadb_operator import ChromaDbOperator
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    print("Creating database")

    doc_type = os.getenv("DOC_TYPE")
    if doc_type is None:
        print("Doc Type not set")
        sys.exit(1)

    doc_file = os.getenv("DATA_FILE")
    if doc_file is None:
        print("Doc File not set")
        sys.exit(1)

    if not os.path.exists(doc_file):
        print(f"Doc File not found:-{doc_file}")
        sys.exit(1)

    embedding_model = os.getenv("EMBEDDING_MODEL")
    if embedding_model is None:
        print("Embedding model not set")
        sys.exit(1)

    ids, docs, metas, embs = [], [], [], []

    match (doc_type):
        case "csv":
            csv_retriever=CSVRetriever(embedding_model)
            ids, docs, metas, embs= csv_retriever.getdata(doc_file)


        case _:
            print(f"Invalid doc type:-{doc_type}")
            sys.exit(1)

    chroma_operator=ChromaDbOperator()
    batch=int(os.getenv("BATCH"))
    db_path=os.getenv("DB_PATH")
    collection_name=os.getenv("COLLECTION_NAME")
    chroma_operator.createdb(ids, docs, metas, embs,batch,db_path,collection_name)

if __name__ == "__main__":
    main()