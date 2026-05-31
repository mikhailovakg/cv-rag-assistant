from langchain_chroma import Chroma


def create_vector_store(chunks, embeddings):

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./vector_store"
    )

    return db