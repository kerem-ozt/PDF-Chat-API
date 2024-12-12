from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from app.services.pdf_service import process_pdf
from app.models.state import pdf_store
from app.core.logger import logger

router = APIRouter()

@router.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")
    if not file.filename.endswith(".pdf"):
        logger.warning("Uploaded file is not a PDF")
        raise HTTPException(status_code=400, detail="File is not a PDF")
    
    try:
        pdf_id = str(uuid.uuid4())
        content = await file.read()
        text, metadata = process_pdf(content, pdf_id)
        pdf_store[pdf_id] = {
            "text": text,
            "metadata": metadata
        }
        logger.info(f"Processed PDF {file.filename} with ID {pdf_id}")
        return {"pdf_id": pdf_id}
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing PDF")
