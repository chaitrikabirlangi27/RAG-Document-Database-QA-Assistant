from src.rag_database.vector_store import create_database_vector_store


def retrieve_schema(question, k=4):
    vector_store = create_database_vector_store()

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return "\n\n".join(
        result.page_content
        for result in results
    )