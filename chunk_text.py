import re

# Read extracted text
with open("syllabus.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Clean extra spaces and empty lines
text = re.sub(r'\n+', '\n', text)
text = re.sub(r'[ \t]+', ' ', text)

# Split into sentences
sentences = re.split(r'(?<=[.!?])\s+', text)

# Create chunks
chunk_size = 1000
overlap = 2

chunks = []
current_chunk = []

for sentence in sentences:

    current_length = sum(len(s) for s in current_chunk)

    if current_length + len(sentence) <= chunk_size:
        current_chunk.append(sentence)

    else:
        chunks.append(" ".join(current_chunk))

        # Keep last 2 sentences as overlap
        current_chunk = current_chunk[-overlap:]
        current_chunk.append(sentence)

# Add remaining text
if current_chunk:
    chunks.append(" ".join(current_chunk))

print("Total chunks:", len(chunks))

# Display first 3 chunks
for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)