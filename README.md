# CampusAI 🎓

> A RAG-powered AI assistant for college students — ask questions about your syllabus and get instant, context-aware answers using **LLaMA 3.2** running locally via Ollama.

![CampusAI UI](https://img.shields.io/badge/UI-Dark%20Theme-7c5cff?style=flat-square) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square) ![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?style=flat-square) ![Ollama](https://img.shields.io/badge/Ollama-LLaMA%203.2-orange?style=flat-square)

---

## ✨ Features

- 🔍 **RAG (Retrieval-Augmented Generation)** — searches your syllabus before answering
- 🦙 **Local LLM** — runs LLaMA 3.2 (3B) via Ollama, fully offline & private
- 🗂️ **ChromaDB** — fast semantic vector search over your documents
- 💬 **Chat UI** — clean dark-mode interface with streaming text, chat history & more
- 📄 **Source citations** — every answer shows which document it came from

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB |
| LLM | LLaMA 3.2 (3B) via Ollama |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed

### 1. Clone the repo

```bash
git clone https://github.com/ish112424/campus-ai.git
cd campus-ai
```

### 2. Create & activate virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask flask-cors chromadb sentence-transformers requests
```

### 4. Add your syllabus

Place your syllabus content in `syllabus.txt` (plain text).

### 5. Populate the vector database

```bash
python store_embeddings.py
```

### 6. Pull the LLaMA model

```bash
ollama pull llama3.2:3b
```

### 7. Start Ollama

```bash
ollama serve
```

### 8. Start the backend

```bash
python backend.py
```

### 9. Open the app

Visit **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 📁 Project Structure

```
campus-ai/
├── backend.py            # Flask API + RAG logic
├── store_embeddings.py   # Chunks syllabus & stores embeddings in ChromaDB
├── extract_pdf.py        # Extracts text from PDFs → syllabus.txt
├── chunk_text.py         # Text chunking utilities
├── embeddings.py         # Embedding helpers
├── rag.py                # RAG query logic
├── test_search.py        # ChromaDB search tester
├── syllabus.txt          # Your college syllabus (plain text)
├── test.html             # Frontend chat UI
├── data/                 # Raw PDF documents
└── extracted/            # Extracted text from PDFs
```

---

## 🔧 How It Works

```
User Question
     │
     ▼
Embed question (all-MiniLM-L6-v2)
     │
     ▼
Search ChromaDB for relevant syllabus chunks
     │
     ▼
Build prompt: [context] + [question]
     │
     ▼
Send to LLaMA 3.2 via Ollama
     │
     ▼
Stream answer back to UI
```

---

## 📝 License

MIT
