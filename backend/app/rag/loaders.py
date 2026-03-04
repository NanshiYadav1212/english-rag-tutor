import fitz, docx

def extract_text(file):
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=file.file.read(),filetype="pdf")
        return "".join(page.get_text() for page in doc)
    
    if file.filename.endswith(".docx"):
        d = docx.Document(file.file)
        return "\n".join(p.text for p in d.paragraphs)
    
    return file.file.read().decode("utf-8")
    