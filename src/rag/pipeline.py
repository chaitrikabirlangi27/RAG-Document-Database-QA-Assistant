from src.rag.chunking import split_text
from src.rag.embeddings import get_embeddings
from src.rag.vector_store import create_vector_store
from src.rag.retriever import create_retriever
from src.rag.prompt import get_rag_prompt
from src.rag.llm import get_llm
from src.rag.chain import create_rag_chain

def build_retrieval_pipeline(document_text):
    """
    Process document text and create a retriever.
    """

    # 1. Split document into chunks
    document_chunks = split_text(document_text)

    # 2. Create embedding model
    embeddings = get_embeddings()

    # 3. Create FAISS vector store
    vector_store = create_vector_store(
        document_chunks,
        embeddings
    )

    # 4. Create retriever
    retriever = create_retriever(vector_store)

    return retriever

def build_rag_chain(retriever):
    """
    Create the complete RAG answer-generation chain.
    """

    prompt = get_rag_prompt()

    llm = get_llm()

    rag_chain = create_rag_chain(
        retriever,
        prompt,
        llm
    )

    return rag_chain