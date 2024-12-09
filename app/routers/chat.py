from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.state import pdf_store
from app.services.llm_service import ask_llm
from app.core.logger import logger

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/v1/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: str, request: ChatRequest):
    logger.info(f"Chat request for PDF ID {pdf_id} with message: {request.message}")
    if pdf_id not in pdf_store:
        logger.warning(f"PDF ID {pdf_id} not found")
        raise HTTPException(status_code=404, detail="PDF not found")
    
    pdf_text = pdf_store[pdf_id]["text"]
    try:
        response = await ask_llm(pdf_text, request.message)
        logger.info(f"Generated response: {response}")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating response")
