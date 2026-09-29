from langchain_ollama import OllamaEmbeddings


def get_embeddings():
    """
    Create and return the local Ollama embedding model.
    """

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    return embeddings