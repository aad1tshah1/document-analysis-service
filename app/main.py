from fastapi import FastAPI

app = FastAPI(title="Document Analysis Service")

@app.get("/health")
def health():
    return {"status": "ok"}
