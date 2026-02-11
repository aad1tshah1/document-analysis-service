from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Document

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str = Field(min_length=1, max_length=300)
    content: str = Field(min_length=1)

class DocumentOut(BaseModel):
    id: str
    title: str 
    description: str 
    content: str
    created_at: str


@router.post("")
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    doc = Document(
        title=payload.title,
        description=payload.description,
        content=payload.content,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {"id": str(doc.id)}

@router.get("/{id}", response_model=DocumentOut)
def get_document(id: UUID, db: Session = Depends(get_db)):
    statement = select(Document).where(Document.id == id)
    document = db.execute(statement).scalar_one_or_none()

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found!")
    
    return {
        "id": str(document.id),
        "title": document.title,
        "description": document.description,
        "content": document.content,
        "created_at": document.created_at.isoformat(),

    }
