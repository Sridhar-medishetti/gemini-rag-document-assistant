import os
import streamlit as st
from src.ingest import load_documents, chunk_documents, save_to_vector_db
from src.query import ask_question


st.set_page_config(
    page_title="Document Q&A Bot",
    page_icon="📚"
)

st.sidebar.title("Project Info")
st.sidebar.info("""
Embedding Model: all-MiniLM-L6-v2

LLM: Gemini 2.5 Flash

Vector DB: ChromaDB
""")

st.markdown("""
### Retrieval-Augmented Generation (RAG)

Upload documents, search semantically, and get grounded answers with citations.
""")

st.title("📚 AI Document Q&A Bot")


def build_database_if_missing():
    db_file_exists = os.path.exists("db/chroma.sqlite3")

    if not db_file_exists:
        with st.spinner("Building vector database for first-time setup..."):
            docs = load_documents("data")
            chunks = chunk_documents(docs)
            save_to_vector_db(chunks)
            st.success("Vector database created successfully!")


build_database_if_missing()

question = st.text_input("Ask a question about your documents")

if st.button("Ask"):
    if question.strip():
        with st.spinner("Searching documents and generating answer..."):
            answer, results = ask_question(question)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources")
        for meta in results["metadatas"][0]:
            st.write(f"📄 {meta['source']} | Page {meta['page']}")
    else:
        st.warning("Please enter a question.")