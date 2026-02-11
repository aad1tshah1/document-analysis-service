from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, func
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

class DocumentListOut(BaseModel):
    items: List[DocumentOut]
    limit: int
    offset: int
    count: int

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

@router.get("", response_model=DocumentListOut)
def list_document(limit:int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    count_statement = select(func.count()).select_from(Document)
    total = db.execute(count_statement).scalar_one()

    statement = select(Document).order_by(Document.created_at.desc()).limit(limit).offset(offset)
    document = db.execute(statement).scalars(all)

    return {
        "items": [ 
            {
            "id": str(doc.id),
            "title": doc.title,
            "description": doc.description,
            "content": doc.content,
            "created_at": doc.created_at.isoformat(),
            }
            for doc in document
        ],
        "limit": limit,
        "offset": offset,
        "count": total,
    }


