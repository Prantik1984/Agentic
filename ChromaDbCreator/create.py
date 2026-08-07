import sys

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

    match (doc_type):
        case "csv":
            print("csv")
        case _:
            print(f"Invalid doc type:-{doc_type}")
            sys.exit(1)

if __name__ == "__main__":
    main()