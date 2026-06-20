import os
import chromadb
from pypdf import PdfReader
from docx import Document
from sentence_transformers import SentenceTransformer


# Embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def extract_pdf(file_path):
    documents = []

    reader = PdfReader(file_path)

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()

        if text and text.strip():
            documents.append({
                "text": text.strip(),
                "metadata": {
                    "source": os.path.basename(file_path),
                    "page": page_num + 1
                }
            })

    return documents


def extract_docx(file_path):
    documents = []

    doc = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    )

    if text.strip():
        documents.append({
            "text": text.strip(),
            "metadata": {
                "source": os.path.basename(file_path),
                "page": 1
            }
        })

    return documents


def load_documents(data_folder="data"):
    all_docs = []

    for file in os.listdir(data_folder):

        path = os.path.join(data_folder, file)

        try:
            if file.endswith(".pdf"):
                all_docs.extend(extract_pdf(path))

            elif file.endswith(".docx"):
                all_docs.extend(extract_docx(path))

        except Exception as e:
            print(f"Skipping {file}: {e}")

    return all_docs


def chunk_documents(documents, chunk_size=1000, overlap=200):

    chunks = []

    for doc in documents:

        text = doc["text"]
        metadata = doc["metadata"]

        start = 0

        while start < len(text):

            end = min(start + chunk_size, len(text))

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "source": metadata["source"],
                    "page": metadata["page"]
                }
            })

            start += (chunk_size - overlap)

    return chunks


def get_embedding(text):
    return embedding_model.encode(text).tolist()


def save_to_vector_db(chunks):

    client = chromadb.PersistentClient(path="db")

    try:
        client.delete_collection("document_knowledge_base")
    except:
        pass

    collection = client.get_or_create_collection(
        name="document_knowledge_base"
    )

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    embeddings = [
        get_embedding(doc)
        for doc in documents
    ]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB")


if __name__ == "__main__":

    docs = load_documents()

    chunks = chunk_documents(docs)

    print(f"Loaded {len(docs)} pages")
    print(f"Created {len(chunks)} chunks")

    save_to_vector_db(chunks)

    for chunk in chunks[:3]:
        print(chunk["metadata"])