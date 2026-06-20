import streamlit as st
from src.query import ask_question

st.set_page_config(
    page_title="Document Q&A Bot",
    page_icon="📚"
)

st.markdown("""
### Retrieval-Augmented Generation (RAG)

Upload documents, search semantically,
and get grounded answers with citations.
""")

st.title("📚 AI Document Q&A Bot")

st.sidebar.title("Project Info")

st.sidebar.info(
"""
Embedding Model:
all-MiniLM-L6-v2

LLM:
Gemini 2.5 Flash

Vector DB:
ChromaDB
"""
)

question = st.text_input(
    "Ask a question about your documents"
)

if st.button("Ask"):

    if question.strip():

        with st.spinner("Searching documents..."):
            answer, results = ask_question(question)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources")

        for meta in results["metadatas"][0]:
            st.write(
                f"📄 {meta['source']} | Page {meta['page']}"
            )

    else:
        st.warning("Please enter a question.")