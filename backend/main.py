from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.transactions import router as transactions_router


app = FastAPI(title="SmartPOS Green AI")


app.include_router(auth_router)
app.include_router(transactions_router)


@app.get("/")
def root():
    return {"message": "SmartPOS Green AI Backend is running"}
