from fastapi import FastAPI
from app.api.api import api_router

app = FastAPI(title="Cinema API")

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
