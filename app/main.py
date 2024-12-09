from fastapi import FastAPI
from app.routers.pdf import router as pdf_router
from app.routers.chat import router as chat_router

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(pdf_router)
app.include_router(chat_router)