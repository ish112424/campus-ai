import pymupdf

pdf_path = "data/pdfs/BTech_CSE_Syllabus.pdf"

doc = pymupdf.open(pdf_path)

text = ""

for page in doc:
    text += page.get_text()
    text += "\n"

doc.close()

# Save to file
with open("syllabus.txt", "w", encoding="utf-8") as f:
    f.write(text)