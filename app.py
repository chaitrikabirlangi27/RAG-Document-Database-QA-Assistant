import streamlit as st
import tempfile

from dotenv import load_dotenv

from src.loaders.document_loader import load_document
from src.rag.pipeline import build_retrieval_pipeline
from src.rag.llm import get_llm
from src.rag.prompt import get_rag_prompt
from src.rag.chain import create_rag_chain


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# Custom Dark Blue / Black Theme
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       FULL APPLICATION BACKGROUND
       ======================================================== */

    .stApp {
        background: linear-gradient(
            135deg,
            #050b14 0%,
            #0a1628 50%,
            #07111f 100%
        );

        color: #f1f5f9;
    }


    /* ========================================================
       STREAMLIT TOP HEADER
       Removes the white area at the top
       ======================================================== */

    [data-testid="stHeader"] {
        background: #050b14;
    }

    header {
        background: #050b14;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }


    /* ========================================================
       MAIN APP VIEW
       ======================================================== */

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


    /* ========================================================
       MAIN CONTENT WIDTH AND SPACING
       ======================================================== */

    .block-container {
        max-width: 1000px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       MAIN TITLE
       ======================================================== */

    h1 {
        color: #ffffff;
        font-size: 42px;
        font-weight: 700;
        letter-spacing: -1px;
    }


    /* ========================================================
       SUBHEADINGS
       ======================================================== */

    h2,
    h3 {
        color: #e2e8f0;
        font-weight: 600;
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    p {
        color: #cbd5e1;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background-color: #0d1b2e;
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 12px;
    }


    /* File uploader label */

    [data-testid="stFileUploader"] label {
        color: #e2e8f0;
    }


    /* ========================================================
       TEXT INPUT CONTAINER
       ======================================================== */

    .stTextInput > div > div {
        background-color: #0d1b2e;
        border-radius: 10px;
    }


    /* ========================================================
       TEXT INPUT FIELD
       ======================================================== */

    .stTextInput input {
        background-color: #10243b;
        color: #ffffff;
        border: 1px solid #2563eb;
        border-radius: 10px;
        padding: 12px;
    }


    /* Placeholder text */

    .stTextInput input::placeholder {
        color: #94a3b8;
    }


    /* Text input when selected */

    .stTextInput input:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 1px #2563eb;
    }


    /* ========================================================
       SUCCESS MESSAGE
       ======================================================== */

    [data-testid="stAlert"] {
        background-color: #0b2927;
        border: 1px solid #176b63;
        border-radius: 10px;
        color: #d1fae5;
    }


    /* ========================================================
       SOURCE EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background-color: #0d1b2e;
        border: 1px solid #1e3a5f;
        border-radius: 10px;
    }


    /* Source text */

    [data-testid="stExpander"] p {
        color: #cbd5e1;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #1e3a5f;
    }


    /* ========================================================
       HIDE STREAMLIT MENU
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }


    /* ========================================================
       HIDE STREAMLIT FOOTER
       ======================================================== */

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

st.title("📚 RAG Document Q&A Assistant")

st.write(
    "Upload a PDF, DOCX, or TXT document and ask questions about it."
)


# ============================================================
# DOCUMENT UPLOADER
# ============================================================

uploaded_file = st.file_uploader(
    "Choose a document",
    type=["pdf", "docx", "txt"]
)


# ============================================================
# CACHE RETRIEVAL PIPELINE
# ============================================================

@st.cache_resource
def get_retriever(document_text):
    return build_retrieval_pipeline(document_text)


# ============================================================
# PROCESS UPLOADED DOCUMENT
# ============================================================

if uploaded_file is not None:

    # Get file extension

    suffix = "." + uploaded_file.name.split(".")[-1]


    # Temporarily save uploaded file

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        temp_file.write(
            uploaded_file.getbuffer()
        )

        temp_file_path = temp_file.name


    # ========================================================
    # EXTRACT TEXT
    # ========================================================

    document_text = load_document(
        temp_file_path
    )


    # ========================================================
    # BUILD RETRIEVAL PIPELINE
    # ========================================================

    retriever = get_retriever(
        document_text
    )


    # ========================================================
    # PROCESSING STATUS
    # ========================================================

    st.success(
        "Document processed and ready."
    )


    # ========================================================
    # QUESTION INPUT
    # ========================================================

    question = st.text_input(
        "Ask a question about the document:"
    )


    # ========================================================
    # GENERATE ANSWER
    # ========================================================

    if question:

        # Create RAG prompt

        prompt = get_rag_prompt()


        # Load Groq LLM

        llm = get_llm()


        # Create RAG chain

        rag_chain = create_rag_chain(
            retriever,
            prompt,
            llm
        )


        # Generate answer

        answer = rag_chain.invoke(
            question
        )


        # ====================================================
        # DISPLAY ANSWER
        # ====================================================

        st.subheader(
            "Answer"
        )

        st.write(
            answer
        )


        # ====================================================
        # RETRIEVE SOURCE DOCUMENTS
        # ====================================================

        source_documents = retriever.invoke(
            question
        )


        # ====================================================
        # DISPLAY SOURCES
        # ====================================================

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