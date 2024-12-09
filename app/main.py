from fastapi import FastAPI, Request
from app.routers import pdf, chat
from app.core import logger
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import fastapi

app = FastAPI()

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return fastapi.responses.JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, please slow down."},
    )

app.include_router(pdf.router)
app.include_router(chat.router)

@app.get("/health")
@limiter.limit("1/minute")
def health_check(request: Request):  # Include request as a parameter
    return {"status": "ok"}
