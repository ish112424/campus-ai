from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

import chromadb
from sentence_transformers import SentenceTransformer
import requests


app = Flask(__name__)
CORS(app)


# ==============================
# Load Embedding Model
# ==============================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


# ==============================
# Connect to ChromaDB
# ==============================

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="college_syllabus"
)

print("ChromaDB connected!")
print("Documents:", collection.count())


# ==============================
# CollegeGPT RAG Function
# ==============================

def ask_college_gpt(question):

    # Convert question into embedding
    question_embedding = model.encode(question).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=1
    )

    # Get relevant document
    context = "\n\n".join(results["documents"][0])

    # Get source PDF
    source = results["metadatas"][0][0]["source"]


    # ==============================
    # Prompt for Llama
    # ==============================

    prompt = f"""
You are CollegeGPT, an AI assistant for college students.

Answer the student's question using ONLY the information
provided in the college document context below.

If the answer is not present in the context, say:

"I could not find this information in the available college documents."

College Document Context:
{context}

Student Question:
{question}

Answer:
"""


    # ==============================
    # Send request to Ollama
    # ==============================

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )


    answer = response.json()["response"]

    return answer, source


# ==============================
# Flask API
# ==============================

@app.route("/")
def index():
    return send_file("test.html")


@app.route("/ask", methods=["GET", "POST"])
def ask():

    if request.method == "GET":
        return jsonify({"message": "CollegeGPT /ask endpoint — send a POST request with JSON body: {\"question\": \"...\"}."})

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "answer": "Please enter a question."
        }), 400

    try:

        answer, source = ask_college_gpt(question)

        return jsonify({
            "answer": answer,
            "source": source
        })

    except requests.exceptions.ConnectionError:

        print("Error: Could not connect to Ollama at http://localhost:11434")

        return jsonify({
            "answer": "⚠️ Could not connect to Ollama.\n\nPlease make sure Ollama is running on your computer (`ollama serve` or launch the Ollama app).",
            "source": "System Check"
        })

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "answer": "Something went wrong while processing your question.",
            "source": "Error"
        }), 500


# ==============================
# Start Server
# ==============================

if __name__ == "__main__":

    print("\n===== CollegeGPT Backend =====")
    print("Server running at http://127.0.0.1:5000")
    print("================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )