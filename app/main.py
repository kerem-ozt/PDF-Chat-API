from fastapi import FastAPI
from app.routers import pdf, chat
from app.core import logger

app = FastAPI()

app.include_router(pdf.router)
app.include_router(chat.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
