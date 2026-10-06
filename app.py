import streamlit as st
import tempfile
import pandas as pd

from dotenv import load_dotenv

from src.loaders.document_loader import load_document
from src.rag.pipeline import build_retrieval_pipeline
from src.rag.llm import get_llm
from src.rag.prompt import get_rag_prompt
from src.rag.chain import create_rag_chain

from src.visualization.document_chart import extract_chart_data
from src.visualization.charts import create_chart

from src.database_pipeline.query import run_database_query


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# Custom Dark Blue / Black Theme
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #050b14 0%,
            #0a1628 50%,
            #07111f 100%
        );
        color: #f1f5f9;
    }

    [data-testid="stHeader"] {
        background: #050b14;
    }

    header {
        background: #050b14;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(
            135deg,
            #050b14 0%,
            #0a1628 50%,
            #07111f 100%
        );
    }

    [data-testid="stMain"] {
        background: transparent;
    }

    .block-container {
        max-width: 1000px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: #ffffff;
        font-size: 42px;
        font-weight: 700;
        letter-spacing: -1px;
    }

    h2,
    h3 {
        color: #e2e8f0;
        font-weight: 600;
    }

    p {
        color: #cbd5e1;
    }

    [data-testid="stFileUploader"] {
        background-color: #0d1b2e;
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 12px;
    }

    [data-testid="stFileUploader"] label {
        color: #e2e8f0;
    }

    .stTextInput > div > div {
        background-color: #0d1b2e;
        border-radius: 10px;
    }

    .stTextInput input {
        background-color: #10243b;
        color: #ffffff;
        border: 1px solid #2563eb;
        border-radius: 10px;
        padding: 12px;
    }

    .stTextInput input::placeholder {
        color: #94a3b8;
    }

    .stTextInput input:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 1px #2563eb;
    }

    [data-testid="stAlert"] {
        background-color: #0b2927;
        border: 1px solid #176b63;
        border-radius: 10px;
        color: #d1fae5;
    }

    [data-testid="stExpander"] {
        background-color: #0d1b2e;
        border: 1px solid #1e3a5f;
        border-radius: 10px;
    }

    [data-testid="stExpander"] p {
        color: #cbd5e1;
    }

    hr {
        border-color: #1e3a5f;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title("📚 RAG Document & Database Q&A Assistant")

st.write(
    "Ask questions from documents or query the connected MySQL database."
)


# ============================================================
# DATA SOURCE SELECTION
# ============================================================

data_source = st.radio(
    "Select Data Source",
    ["Document", "Database"],
    horizontal=True
)


# ============================================================
# RETRIEVER
# ============================================================

retriever = None


# ============================================================
# DOCUMENT MODE - FILE UPLOAD
# ============================================================

if data_source == "Document":

    uploaded_file = st.file_uploader(
        "Choose a document",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file is not None:

        # ====================================================
        # GET FILE EXTENSION
        # ====================================================

        suffix = "." + uploaded_file.name.split(".")[-1]


        # ====================================================
        # TEMPORARILY SAVE UPLOADED FILE
        # ====================================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_file_path = temp_file.name


        # ====================================================
        # EXTRACT TEXT
        # ====================================================

        document_text = load_document(
            temp_file_path
        )


        # ====================================================
        # BUILD RETRIEVAL PIPELINE
        # ====================================================

        retriever = build_retrieval_pipeline(
            document_text
        )


        # ====================================================
        # PROCESSING STATUS
        # ====================================================

        st.success(
            "Document processed and ready."
        )


# ============================================================
# QUESTION INPUT
# ============================================================

if data_source == "Document":

    question_label = "Ask a question about the document:"

else:

    question_label = "Ask a question about the database:"


question = st.text_input(
    question_label
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # ========================================================
    # DOCUMENT MODE
    # ========================================================

    if data_source == "Document":

        # ----------------------------------------------------
        # Check document
        # ----------------------------------------------------

        if retriever is None:

            st.warning(
                "Please upload a document first."
            )

        else:

            # =================================================
            # CREATE RAG PROMPT
            # =================================================

            prompt = get_rag_prompt()


            # =================================================
            # LOAD GROQ LLM
            # =================================================

            llm = get_llm()


            # =================================================
            # CREATE RAG CHAIN
            # =================================================

            rag_chain = create_rag_chain(
                retriever,
                prompt,
                llm
            )


            # =================================================
            # GENERATE ANSWER
            # =================================================

            answer = rag_chain.invoke(
                question
            )


            # =================================================
            # RETRIEVE SOURCE DOCUMENTS
            # =================================================

            source_documents = retriever.invoke(
                question
            )


            # =================================================
            # DISPLAY ANSWER
            # =================================================

            st.subheader(
                "Answer"
            )

            st.write(
                answer
            )


            # =================================================
            # GENERATE DOCUMENT CHART
            # =================================================

            try:

                chart_context = "\n\n".join(
                    document.page_content
                    for document in source_documents
                )


                chart_data = extract_chart_data(
                    chart_context,
                    question
                )


                if (
                    chart_data["chart_type"]
                    and chart_data["data"]
                ):

                    chart_dataframe = pd.DataFrame(
                        chart_data["data"]
                    )


                    columns = list(
                        chart_dataframe.columns
                    )


                    if len(columns) >= 2:

                        x_column = columns[0]


                        numeric_columns = (
                            chart_dataframe
                            .select_dtypes(
                                include="number"
                            )
                            .columns
                            .tolist()
                        )


                        if numeric_columns:

                            y_column = numeric_columns[0]


                            chart = create_chart(
                                dataframe=chart_dataframe,
                                chart_type=chart_data["chart_type"],
                                x_column=x_column,
                                y_column=y_column,
                                title=chart_data["title"]
                            )


                            if chart is not None:

                                st.subheader(
                                    "Visualization"
                                )

                                st.plotly_chart(
                                    chart,
                                    use_container_width=True
                                )


            except Exception as e:

                st.error(
                    f"Chart generation failed: {e}"
                )


            # =================================================
            # DISPLAY SOURCES
            # =================================================

            st.subheader(
                "Sources"
            )


            for index, document in enumerate(
                source_documents,
                start=1
            ):

                with st.expander(
                    f"Source {index}"
                ):

                    st.write(
                        document.page_content
                    )


    # ========================================================
    # DATABASE MODE
    # ========================================================

    elif data_source == "Database":

        try:

            # =================================================
            # RUN DATABASE QUERY
            # =================================================

            sql, dataframe, chart = run_database_query(
                question
            )


            # =================================================
            # DISPLAY QUERY RESULT
            # =================================================

            st.subheader(
                "Query Result"
            )


            if dataframe.empty:

                st.write(
                    "No results found."
                )

            else:

                st.dataframe(
                    dataframe,
                    use_container_width=True
                )


            # =================================================
            # DISPLAY GENERATED SQL
            # =================================================

            with st.expander(
                "Generated SQL"
            ):

                st.code(
                    sql,
                    language="sql"
                )


            # =================================================
            # DISPLAY DATABASE CHART
            # =================================================

            if chart is not None:

                st.subheader(
                    "Visualization"
                )

                st.plotly_chart(
                    chart,
                    use_container_width=True
                )


        except Exception as e:

            st.error(
                f"Database query failed: {e}"
            )