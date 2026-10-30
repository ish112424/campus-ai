import chromadb
from sentence_transformers import SentenceTransformer
import requests

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="college_syllabus"
)


def ask_college_gpt(question):

    # Convert question into embedding
    question_embedding = model.encode(question).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=1
    )

    # Get relevant syllabus information
    context = "\n\n".join(results["documents"][0])

    # Prompt for Llama
    prompt = f"""
You are CollegeGPT, an AI assistant for college students.

Answer the student's question using ONLY the information provided
in the syllabus context below.

If the answer is not present in the context, say:
"I could not find this information in the available college documents."

Syllabus Context:
{context}

Student Question:
{question}

Answer:
"""

    # Send prompt to Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


print("\n===== CollegeGPT =====")
print("Ask questions about your college syllabus.")
print("Type 'exit' to stop.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("CollegeGPT: Goodbye!")
        break

    answer = ask_college_gpt(question)

    print("\nCollegeGPT:")
    print(answer)
    print()