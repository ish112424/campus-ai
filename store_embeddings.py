import re
import chromadb
from sentence_transformers import SentenceTransformer


# -------------------------------
# 1. Read the syllabus text
# -------------------------------

with open("syllabus.txt", "r", encoding="utf-8") as file:
    text = file.read()


# -------------------------------
# 2. Clean the text
# -------------------------------

text = re.sub(r'\n+', '\n', text)
text = re.sub(r'[ \t]+', ' ', text)


# -------------------------------
# 3. Split text into sentences
# -------------------------------

sentences = re.split(r'(?<=[.!?])\s+', text)


# -------------------------------
# 4. Create chunks
# -------------------------------

chunk_size = 1000
overlap = 2

chunks = []
current_chunk = []

for sentence in sentences:

    current_length = sum(len(s) for s in current_chunk)

    if current_length + len(sentence) <= chunk_size:
        current_chunk.append(sentence)

    else:
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        current_chunk = current_chunk[-overlap:]
        current_chunk.append(sentence)


# Add the final chunk
if current_chunk:
    chunks.append(" ".join(current_chunk))


print("Total chunks:", len(chunks))


# -------------------------------
# 5. Load embedding model
# -------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------------
# 6. Create embeddings
# -------------------------------

print("Creating embeddings...")

embeddings = model.encode(chunks)

print("Embeddings created!")


# -------------------------------
# 7. Create ChromaDB
# -------------------------------

print("Creating ChromaDB...")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="college_syllabus"
)


# -------------------------------
# 8. Store chunks + embeddings
# -------------------------------

collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings.tolist(),
    metadatas=[{"source": "syllabus.txt"} for _ in chunks]
)


print("Successfully stored data in ChromaDB!")
print("Total documents:", collection.count())