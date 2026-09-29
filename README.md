# 🧠 RAG Document Q&A Assistant

A Retrieval-Augmented Generation (RAG) based document question-answering application built with Python, LangChain, FAISS, Ollama, Groq, and Streamlit.

The application allows users to upload a PDF, DOCX, or TXT document and ask questions about its content. It retrieves the most relevant parts of the uploaded document and uses an LLM to generate an answer based on the retrieved context.

---

## 📌 Project Overview

Traditional LLM applications may not have access to the contents of a user's private documents.

This project uses **Retrieval-Augmented Generation (RAG)** to solve this problem.

Instead of sending the complete document to the LLM for every question, the application:

1. Extracts text from the uploaded document.
2. Splits the text into smaller chunks.
3. Converts the chunks into embeddings.
4. Stores the embeddings in a FAISS vector store.
5. Retrieves the most relevant chunks for a user's question.
6. Sends the retrieved context and question to the LLM.
7. Generates an answer using the retrieved document information.
8. Displays the retrieved source chunks to the user.

---

## ✨ Features

- 📄 Upload PDF documents
- 📝 Upload DOCX documents
- 📃 Upload TXT documents
- 🔍 Semantic similarity-based retrieval
- 🧩 Automatic text chunking
- 🧠 Local text embeddings using Ollama
- 🗃️ FAISS vector similarity search
- 🤖 Groq LLM for answer generation
- 🔗 LangChain-based RAG pipeline
- 💬 Ask multiple questions about the uploaded document
- 📚 Display retrieved source chunks
- 🎨 Dark blue/black Streamlit interface
- 🔐 API key stored using environment variables

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web interface |
| LangChain | RAG pipeline and component integration |
| FAISS | Vector similarity search |
| Ollama | Local embedding generation |
| Nomic Embed Text | Embedding model |
| Groq | LLM inference |
| PyPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| python-dotenv | Environment variable management |

---

## 🏗️ System Architecture

```text
                User
                  │
                  ▼
       Upload PDF / DOCX / TXT
                  │
                  ▼
          Document Loader
                  │
                  ▼
            Text Extraction
                  │
                  ▼
              Chunking
                  │
                  ▼
       Local Embeddings
       Ollama + Nomic
                  │
                  ▼
          FAISS Vector Store
                  │
                  ▼
             Retriever
                  │
                  │
        User asks a question
                  │
                  ▼
       Retrieve relevant chunks
                  │
                  ▼
        RAG Prompt + Context
                  │
                  ▼
            Groq LLM
                  │
                  ▼
             Answer
                  │
                  ▼
        Retrieved Sources