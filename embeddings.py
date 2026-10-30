import os
import re
import chromadb
from sentence_transformers import SentenceTransformer
import pymupdf


# --------------------------------
# Settings
# --------------------------------

PDF_FOLDER = "data/pdfs"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "college_syllabus"


# --------------------------------
# Load embedding model
# --------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")


# --------------------------------
# Read all PDFs
# --------------------------------

all_chunks = []
all_ids = []
all_metadatas = []

pdf_files = [
    file for file in os.listdir(PDF_FOLDER)
    if file.lower().endswith(".pdf")
]

print("\nPDF files found:", len(pdf_files))

for pdf_file in pdf_files:

    pdf_path = os.path.join(PDF_FOLDER, pdf_file)

    print(f"\nProcessing: {pdf_file}")

    doc = pymupdf.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()
        text += "\n"

    doc.close()

    # Clean text
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # --------------------------------
    # Create chunks
    # --------------------------------

    chunk_size = 1000
    overlap = 2

    chunks = []
    current_chunk = []

    for sentence in sentences:

        current_length = sum(
            len(s) for s in current_chunk
        )

        if current_length + len(sentence) <= chunk_size:

            current_chunk.append(sentence)

        else:

            if current_chunk:
                chunks.append(
                    " ".join(current_chunk)
                )

            current_chunk = current_chunk[-overlap:]
            current_chunk.append(sentence)

    if current_chunk:
        chunks.append(
            " ".join(current_chunk)
        )

    print("Chunks created:", len(chunks))

    # --------------------------------
    # Store chunks + metadata
    # --------------------------------

    for i, chunk in enumerate(chunks):

        all_chunks.append(chunk)

        all_ids.append(
            f"{pdf_file}_chunk_{i}"
        )

        all_metadatas.append({
            "source": pdf_file
        })


# --------------------------------
# Create embeddings
# --------------------------------

print("\nCreating embeddings...")

embeddings = model.encode(all_chunks)

print("Embeddings created!")


# --------------------------------
# Connect to ChromaDB
# --------------------------------

print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# Delete old collection
try:

    client.delete_collection(
        name=COLLECTION_NAME
    )

    print("Old collection deleted.")

except:

    pass


# Create new collection
collection = client.create_collection(
    name=COLLECTION_NAME
)


# --------------------------------
# Store everything
# --------------------------------

collection.add(

    ids=all_ids,

    documents=all_chunks,

    embeddings=embeddings.tolist(),

    metadatas=all_metadatas

)


print("\n================================")
print("All PDFs stored successfully!")
print("================================")

print("Total PDFs:", len(pdf_files))
print("Total chunks:", len(all_chunks))
print("ChromaDB documents:", collection.count())