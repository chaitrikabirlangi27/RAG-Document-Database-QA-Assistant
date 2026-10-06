def create_retriever(vector_store):
    """
    Create a retriever from the FAISS vector store.
    """

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 10}
    )

    return retriever
