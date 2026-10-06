from langchain_community.vectorstores import FAISS

from src.database.schema import (
    get_database_schema,
    format_schema_for_rag,
)
from src.rag_database.embeddings import embeddings


def create_database_vector_store():
    schema = get_database_schema()

    formatted_schema = format_schema_for_rag(schema)

    schema_texts = formatted_schema.split("\n\n")

    vector_store = FAISS.from_texts(
        texts=schema_texts,
        embedding=embeddings
    )

    return vector_store