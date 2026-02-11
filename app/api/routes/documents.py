from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Document

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=300)
    content: str = Field(min_length=1)


@router.post("")
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    doc = Document(
        title=payload.title,
        description=payload.description,
        content=payload.content,
    )
    db.add(doc)
    db.commit()
    # db.refresh(doc)

    return {"id": str(doc.id)}
