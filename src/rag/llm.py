from langchain_groq import ChatGroq


def get_llm():
    """
    Create and return the Groq LLM.
    """

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    return llm