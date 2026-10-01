from fastapi import FastAPI

app = FastAPI(title="SmartPOS Green AI")


@app.get("/")
def root():
    return {"message": "SmartPOS Green AI Backend is running"}