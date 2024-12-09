from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.state import pdf_store
from app.services.llm_service import ask_llm

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/v1/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: str, request: ChatRequest):
    # print(pdf_store)
    if pdf_id not in pdf_store:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    pdf_text = pdf_store[pdf_id]["text"]
    # print(pdf_text)
    # return 1
    response = await ask_llm(pdf_text, request.message)
    return {"response": response}
