from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import MODEL_WEIGHTS_DIR, PERSIST_DIR


class EmbeddingModel:
    def __init__(
        self,
        model_name: str = "all-mpnet-base-v2",
        collection_name: str = "carakasamhita_embeddings",
    ):
        """
        Initializes the embedding model.

        Args:
            model_name (str): The name of the embedding model to use. Default: "all-mpnet-base-v2".
        """
        self.model_name = model_name
        self.collection_name = collection_name
        self.embedding_model = None
        self.embeddings = None
        self.vector_store = None
        self.load_model()

    def load_model(self):
        if self.embedding_model is not None:
            print(f"Model {self.model_name} is already loaded.")
            return
        try:
            print(f"Loading embedding model {self.model_name}...")
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=self.model_name, cache_folder=MODEL_WEIGHTS_DIR
            )
            print(f"Model {self.model_name} loaded successfully.")
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            self.embedding_model = None

    def encode(self, texts: list[str]) -> list[list[float]]:
        """
        Encodes a list of texts into embeddings.

        Args:
            texts (list): A list of strings to encode.

        Returns:
            list: A list of embeddings corresponding to the input texts.
        """
        if self.embedding_model is None:
            raise ValueError("Model is not loaded. Please load the model first.")
        self.embeddings = self.embedding_model.encode(
            texts, convert_to_tensor=True
        ).tolist()
        return self.embeddings

    def save_embeddings(
        self, docs: list[Document], persist_directory: str = PERSIST_DIR
    ) -> Chroma:
        """
        Saves the embeddings to a Chroma vector store.

        Args:
            docs (list): A list of Document objects to save.
            persist_directory (str): The directory where the Chroma database will be stored. Default: PERSIST_DIR set in config.py.

        Returns:
            Chroma: The vector store containing the saved embeddings.
        """
        if self.embedding_model is None:
            raise ValueError("Model is not loaded. Please load the model first.")

        if self.vector_store is not None:
            print(
                f"Vector store for collection '{self.collection_name}' already exists. It will be overwritten."
            )

        print(
            f"Saving embeddings to {persist_directory} in collection '{self.collection_name}'..."
        )
        self.vector_store = Chroma.from_documents(
            documents=docs,
            embedding=self.embedding_model,
            collection_name=self.collection_name,
            persist_directory=persist_directory,
        )
        print(
            f"Embeddings saved to {persist_directory} in collection '{self.collection_name}'."
        )
        return self.vector_store

    def load_embeddings(self, persist_directory: str = PERSIST_DIR) -> Chroma:
        """
        Loads embeddings from a Chroma vector store.

        Args:
            collection_name (str): The name of the collection to load the embeddings from.
            persist_directory (str): The directory where the Chroma database is stored. Default: "data/store/chroma_db".

        Returns:
            Chroma: The loaded vector store.
        """
        if self.vector_store is not None:
            print(
                f"Vector store for collection '{self.collection_name}' already exists. It will be overwritten."
            )

        self.vector_store = Chroma(
            embedding_function=self.embedding_model,
            collection_name=self.collection_name,
            persist_directory=persist_directory,
        )
        print(
            f"Embeddings loaded from {persist_directory} in collection '{self.collection_name}'."
        )
        return self.vector_store

    def get_retriever(self, k: int = 3, fetch_k: int = 10) -> VectorStoreRetriever:
        """
        Returns a retriever for the vector store, using MMR (Maximal Marginal Relevance) search.

        Args:
            k (int): The number of top results to return. Default: 3.
            fetch_k (int): The number of results to fetch before applying MMR. Default: 10.

        Returns:
            VectorStoreRetriever: A retriever for the vector store.
        """
        if self.vector_store is None:
            raise ValueError(
                "Vector store is not loaded. Please load the vector store first."
            )

        return self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": fetch_k,
            },
        )

    def query(self, query: str, k: int = 5) -> list[Document]:
        """
        Queries the vector store for the top k most similar documents to the query.

        Args:
            query (str): The query string to search for.
            k (int): The number of top results to return. Default: 5.

        Returns:
            list: A list of the top k most similar documents.
        """
        if self.vector_store is None:
            raise ValueError(
                "Vector store is not loaded. Please load the vector store first."
            )

        results = self.vector_store.similarity_search(query, k=k)
        return results
