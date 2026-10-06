# 🧠 RAG Document & Database Q&A Assistant

A Retrieval-Augmented Generation (RAG) based application that allows users to ask questions from uploaded documents or query a connected MySQL database using natural language.

The application combines:

- Document-based RAG
- Database schema retrieval
- Natural-language-to-SQL generation
- MySQL query execution
- Data visualization

The system uses local embeddings with Ollama and Nomic Embed Text, FAISS for vector similarity search, Groq for LLM inference, LangChain for the RAG pipeline, and Streamlit for the user interface.

---

## 📌 Project Overview

The application supports two data sources:

1. **Documents** — PDF, DOCX, and TXT files
2. **MySQL Database** — structured relational data

Users can select the required data source and ask questions using natural language.

### Document Mode

The application:

1. Loads the uploaded document.
2. Extracts its text.
3. Splits the text into smaller chunks.
4. Converts the chunks into embeddings.
5. Stores the embeddings in a FAISS vector store.
6. Retrieves the most relevant chunks for the user's question.
7. Sends the retrieved context to the LLM.
8. Generates an answer based only on the retrieved document context.
9. Displays the retrieved source chunks.
10. Generates visualizations when numerical information from the document is requested as a chart.

### Database Mode

The application:

1. Connects to a MySQL database.
2. Reads the database schema and table relationships.
3. Converts schema information into embeddings.
4. Stores the schema embeddings in FAISS.
5. Retrieves the most relevant schema information for the user's question.
6. Uses the LLM to generate a MySQL SELECT query.
7. Validates the generated SQL query.
8. Executes the query against MySQL.
9. Displays the query results.
10. Generates visualizations from the actual query results when requested.

---

## ✨ Features

### 📄 Document Q&A

- Upload PDF documents
- Upload DOCX documents
- Upload TXT documents
- Semantic similarity-based retrieval
- Automatic text chunking
- Local text embeddings using Ollama
- FAISS vector similarity search
- Groq LLM for answer generation
- Retrieved source display
- Document-based chart generation

### 🗄️ Database Q&A

- Connect to MySQL
- Automatically inspect database tables and columns
- Detect foreign-key relationships
- Retrieve relevant database schema using FAISS
- Natural-language-to-SQL generation
- MySQL SELECT query execution
- Display generated SQL
- Display query results as a table
- Support relational queries involving JOINs

### 📊 Data Visualization

The application can generate:

- Bar charts
- Pie charts
- Line charts
- Scatter plots

Charts are generated from actual document or database data rather than fabricated values.

### 🔐 Safety

- Database operations are read-only
- Only SELECT queries are allowed
- INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, and other write operations are blocked
- API keys and database credentials are stored using environment variables
- `.env` is excluded from Git

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web interface |
| LangChain | RAG pipeline and LLM integration |
| FAISS | Vector similarity search |
| Ollama | Local embedding generation |
| Nomic Embed Text | Local embedding model |
| Groq | LLM inference |
| MySQL | Relational database |
| SQLAlchemy | Database connection and execution |
| PyMySQL | MySQL driver |
| Pandas | Data processing and tabular results |
| Plotly | Data visualization |
| PyPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| python-dotenv | Environment variable management |

---

## 🏗️ System Architecture

```text
                         User
                           │
                           ▼
                  Select Data Source
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
        DOCUMENT                     DATABASE
             │                           │
      PDF / DOCX / TXT                 MySQL
             │                           │
             ▼                           ▼
     Document Loader             Schema Inspection
             │                           │
             ▼                           ▼
       Text Extraction            Schema Formatting
             │                           │
             ▼                           ▼
          Chunking                Schema Embeddings
             │                           │
             ▼                           ▼
      Local Embeddings                 FAISS
      Ollama + Nomic                    │
             │                          ▼
             ▼                    Schema Retrieval
            FAISS                       │
             │                          ▼
             ▼                    SQL Generation
        Retrieval                       │
             │                          ▼
             ▼                    SQL Validation
       RAG Prompt                       │
             │                          ▼
             ▼                    MySQL Execution
          Groq                          │
             │                          ▼
             ▼                    Query Results
          Answer                        │
             │                          │
             └─────────────┬────────────┘
                           ▼
                    Answer / Results
                           │
                           ▼
                    Data Visualization