from sentence_transformers import SentenceTransformer

class TextEmbedder:

    def __init__(self,embedding_model):
        self.model = SentenceTransformer(
            embedding_model
        )



    def embed_text(self, text:str):
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()






