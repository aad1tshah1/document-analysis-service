from fastapi import FastAPI

from app.db.models import Base
from app.db.session import engine
from app.api.routes.documents import router as documents_router
from app.api.routes.analysis_jobs import router as analysis_jobs_router

app = FastAPI(title="Document Analysis Service")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(documents_router)
app.include_router(analysis_jobs_router)


@app.get("/health")
def health():
    return {"status": "ok"}
