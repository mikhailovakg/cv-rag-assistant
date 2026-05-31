from pathlib import Path

import streamlit as st

from src.ingest import load_pdf
from src.chunking import split_documents
from src.embeddings import get_embeddings
from src.vector_store import create_vector_store
from src.retriever import get_retriever
from src.llm import get_llm
from src.rag import build_context

from src.job_extractor import extract_job_text
from src.job_cleaner import clean_job_text
from src.job_match import build_job_match_prompt

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="CV RAG Assistant",
    page_icon="📄"
)

st.title("📄 CV RAG Assistant")

# ==================================================
# CV UPLOAD
# ==================================================

st.header("📄 CV Upload")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file:

    file_path = UPLOAD_DIR / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ----------------------------------------------
    # Document Processing
    # ----------------------------------------------

    docs = load_pdf(str(file_path))

    chunks = split_documents(docs)

    st.success(f"Loaded {len(docs)} pages")
    st.info(f"Created {len(chunks)} chunks")

    embeddings = get_embeddings()

    db = create_vector_store(
        chunks,
        embeddings
    )

    st.success("Vector database created")

    # ----------------------------------------------
    # CV CHAT
    # ----------------------------------------------

    st.header("🤖 Chat With Your CV")

    question = st.text_input(
        "Ask a question about your CV",
        key="cv_question"
    )

    if question:

        retriever = get_retriever(db)

        results = retriever.invoke(question)

        context = build_context(results)

        llm = get_llm()

        prompt = f"""
You are a CV assistant.

Answer only using the supplied context.

If the answer cannot be found in the context,
say so.

Context:
{context}

Question:
{question}
"""

        response = llm.invoke(prompt)

        st.subheader("Answer")

        st.write(response.content)

    # ----------------------------------------------
    # JOB MATCH
    # ----------------------------------------------

    st.header("💼 Job Match Analysis")

    job_url = st.text_input(
        "Job Posting URL",
        key="job_url"
    )

    if st.button(
        "Analyze Job",
        key="analyze_job"
    ):

        try:

            raw_job_text = extract_job_text(job_url)

            job_text = clean_job_text(raw_job_text)

            retriever = get_retriever(db)

            results = retriever.invoke(job_text)

            cv_context = build_context(results)

            prompt = build_job_match_prompt(
                cv_context,
                job_text
            )

            llm = get_llm()

            response = llm.invoke(prompt)

            st.subheader("Job Match Report")

            st.write(response.content)

            with st.expander(
                "Retrieved CV Context"
            ):

                for doc in results:
                    st.write(doc.page_content)

        except Exception as e:

            st.error(
                f"Failed to analyze job: {e}"
            )

    # ----------------------------------------------
    # DEBUG SECTION
    # ----------------------------------------------

    with st.expander("PDF Preview"):

        st.write(
            docs[0].page_content[:2000]
        )

    with st.expander("Chunk Preview"):

        for i, chunk in enumerate(chunks[:3]):

            st.markdown(
                f"### Chunk {i + 1}"
            )

            st.write(chunk.page_content)
