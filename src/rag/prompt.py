from langchain_core.prompts import ChatPromptTemplate


def get_rag_prompt():
    """
    Create the prompt used by the RAG system.
    """

    prompt = ChatPromptTemplate.from_template(
        """
You are a document question-answering assistant.

Answer the user's question using only the information provided
in the context below.

If the answer cannot be found in the context, say:
"I could not find the answer in the uploaded document."

Do not use outside knowledge.
Keep the answer clear and concise.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    return prompt