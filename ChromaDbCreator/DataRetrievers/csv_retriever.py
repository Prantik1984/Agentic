import os


class CSVRetriever:
    def getdata(self,csv_file:str):
        """"
        reads the csv file and returns the docs and metadatas that
        need to be upserted to the chromadb
        """
        if not os.path.exists(csv_file):
            print(f"File {csv_file} does not exist")
            return None

