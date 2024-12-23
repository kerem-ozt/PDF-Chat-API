from pypdf import PdfReader
from io import BytesIO
from app.core.logger import logger
from app.utils.pdf_utils import preprocess_text
from app.services.rag_service import store_pdf_chunks

def process_pdf(pdf_content: bytes, pdf_id: str):
    try:
        reader = PdfReader(BytesIO(pdf_content))
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        full_text = "\n".join(text)
        full_text = preprocess_text(full_text)
        metadata = {
            "num_pages": len(reader.pages),
            "title": reader.metadata.title if reader.metadata.title else "Untitled",
            "author": reader.metadata.author if reader.metadata.author else "Unknown"
        }
        logger.info(f"Extracted text from PDF: {metadata}")
        
        store_pdf_chunks(pdf_id, full_text)

        return full_text, metadata
    except Exception as e:
        logger.error(f"Failed to process PDF: {str(e)}")
        raise e
