import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from src.config import GEMINI_API_KEY


embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

client = genai.Client(api_key=GEMINI_API_KEY)


def search_documents(query, k=3):
    db_client = chromadb.PersistentClient(path="db")

    collection = db_client.get_collection(
        name="document_knowledge_base"
    )

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results


def generate_answer(question, results):
    context_blocks = []

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context_blocks.append(
            f"[Source: {meta['source']}, Page: {meta['page']}]\n{doc}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""
You are a precise document Q&A assistant.

Use ONLY the provided document context to answer the question.
If the answer is not present in the context, say:
"I cannot find the answer in the provided documents."

Always include source citations using filename and page number.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def ask_question(question):
    results = search_documents(question)
    answer = generate_answer(question, results)
    return answer, results


if __name__ == "__main__":
    question = input("Ask a question: ")
    answer, results = ask_question(question)

    print("\nAnswer:\n")
    print(answer)

    print("\nSources Used:\n")
    for meta in results["metadatas"][0]:
        print(f"- {meta['source']}, Page {meta['page']}")