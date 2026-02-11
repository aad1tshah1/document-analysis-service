from fastapi import FastAPI

from app.db.models import Base
from app.db.session import engine
from app.api.routes.documents import router as documents_router

app = FastAPI(title="Document Analysis Service")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(documents_router)


@app.get("/health")
def health():
    return {"status": "ok"}
