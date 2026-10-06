import json
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


def extract_chart_data(context, question):
    prompt = f"""
You are a data extraction assistant.

The user wants to create a chart from information contained in a document.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

Your task is to extract ONLY the numerical data explicitly present
in the document context that is relevant to the user's chart request.

Do not invent or estimate any values.

Return ONLY valid JSON in this exact format:

{{
    "chart_type": "bar",
    "title": "chart title",
    "x_column": "category",
    "y_column": "value",
    "data": [
        {{
            "category": "example",
            "value": 10
        }}
    ]
}}

Rules:
1. Use only information from the document context.
2. Do not invent values.
3. Convert numerical values to numbers.
4. If the requested information is not present, return:
{{
    "chart_type": null,
    "title": null,
    "x_column": null,
    "y_column": null,
    "data": []
}}
5. Return JSON only.
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    return json.loads(content)