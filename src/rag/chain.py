from langchain_core.output_parsers import StrOutputParser


def create_rag_chain(retriever, prompt, llm):
    """
    Create the RAG chain that connects retrieval, prompt, and LLM.
    """

    def format_docs(documents):
        return "\n\n".join(
            document.page_content for document in documents
        )

    def retrieve_and_format(question):
        documents = retriever.invoke(question)
        return format_docs(documents)

    rag_chain = (
        {
            "context": retrieve_and_format,
            "question": lambda question: question
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain