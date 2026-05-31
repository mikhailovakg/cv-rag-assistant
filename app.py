from pathlib import Path
import streamlit as st
from src.ingest import load_pdf

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="CV RAG Assistant",
    page_icon="📄"
)

st.title("📄 CV RAG Assistant")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file:

    file_path = UPLOAD_DIR / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    docs = load_pdf(str(file_path))

    st.success(f"Loaded {len(docs)} pages")

    st.subheader("Preview")

    st.write(docs[0].page_content[:2000])