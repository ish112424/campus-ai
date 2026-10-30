import chromadb
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="college_syllabus"
)


# Student's question
question = "What is the course code for Deep Learning?"


# Convert question into an embedding
question_embedding = model.encode(question).tolist()


# Search ChromaDB
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)


# Display results
print("\nQuestion:")
print(question)

print("\nMost relevant syllabus information:\n")

for i, document in enumerate(results["documents"][0]):
    print(f"--- Result {i + 1} ---")
    print(document)
    print()