from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.models.state import pdf_store
from app.services.llm_service import ask_llm
from app.core.logger import logger
from slowapi.util import get_remote_address
from slowapi import Limiter

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

class ChatRequest(BaseModel):
    message: str

@router.post("/v1/chat/{pdf_id}")
@limiter.limit("3/minute")
async def chat_with_pdf(pdf_id: str, chat_request: ChatRequest, request: Request):
    logger.info(f"Chat request for PDF ID {pdf_id} with message: {chat_request.message}")
    if pdf_id not in pdf_store:
        logger.warning(f"PDF ID {pdf_id} not found")
        raise HTTPException(status_code=404, detail="PDF not found")
    
    pdf_text = pdf_store[pdf_id]["text"]
    try:
        response = await ask_llm(pdf_text, chat_request.message)
        logger.info(f"Generated response: {response}")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating response")
