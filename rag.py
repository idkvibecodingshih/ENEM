import os
import chromadb
from sentence_transformers import (
    SentenceTransformer
)

class RAG:
    def __init__(self):

        self.embedding_model = (
            SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        )

        self.client = (
            chromadb.PersistentClient(
                path="./vector_db"
            )
        )

        self.collection = (
            self.client.get_or_create_collection(
                "knowledge"
            )
        )

        self.add_knowledge()

        
        print("RAG module initialized")
        
    def search(self, query):
        query_embedding = self.embedding_model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )

        docs = results["documents"][0]
        distances = results["distances"][0]

        return docs,distances
    

    def add_knowledge(self):
        for filename in os.listdir("./knowledge"):
            if filename.endswith(".txt"):
                with open(os.path.join("./knowledge", filename), "r", encoding="utf-8") as f:
                    content = f.read()
                    self.collection.add(
                        documents=[content],
                        metadatas={"source": filename},
                        ids=[filename]
                    )