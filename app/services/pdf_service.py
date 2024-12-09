from pypdf import PdfReader
from io import BytesIO

def process_pdf(pdf_content: bytes):
    reader = PdfReader(BytesIO(pdf_content))
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    full_text = "\n".join(text)
    metadata = {
        "num_pages": len(reader.pages)
    }
    return full_text, metadata
