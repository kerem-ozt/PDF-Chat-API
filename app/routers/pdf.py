from fastapi import APIRouter, UploadFile, File
import uuid
from app.services.pdf_service import process_pdf

router = APIRouter()

@router.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "File is not a PDF"}

    pdf_id = str(uuid.uuid4())
    content = await file.read()
    text, metadata = process_pdf(content)

    # Bu text ve metadata'yı bir global state'e saklayabilirsin, örn:
    # state[<pdf_id>] = {"text": text, "metadata": metadata}
    # İleride veritabanı veya in-memory store kullanabilirsin.

    #???
    print(text)
    print(metadata)

    from app.models.state import pdf_store

    pdf_store[pdf_id] = {
        # "text": full_text,
        "text": text,
        "metadata": metadata
    }

    return {"pdf_id": pdf_id}
