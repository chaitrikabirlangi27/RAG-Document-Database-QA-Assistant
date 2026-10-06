import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.rag_database.retriever import retrieve_schema
from src.sql_generation.prompt import sql_prompt


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


def generate_sql(question):
    schema = retrieve_schema(question)

    prompt = sql_prompt.format(
        schema=schema,
        question=question,
    )

    response = llm.invoke(prompt)

    return response.content.strip() 