from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Document, AnalysisJob, AnalysisStatus, AnalysisType

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

class AnalysisJobCreate(BaseModel):
    analysis_type: AnalysisType

class AnalysisJobOut(BaseModel):
    id: str
    document_id: str
    analysis_type: AnalysisType
    status: AnalysisStatus
    created_at: str

@router.post("")
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    document = Document(
        title=payload.title,
        description=payload.description,
        content=payload.content,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    return {"id": str(document.id)}

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
    documents = db.execute(statement).scalars().all()

    return {
        "items": [ 
            {
            "id": str(doc.id),
            "title": doc.title,
            "description": doc.description,
            "content": doc.content,
            "created_at": doc.created_at.isoformat(),
            }
            for doc in documents
        ],
        "limit": limit,
        "offset": offset,
        "count": total,
    }

@router.post("/{document_id}/analysis-jobs", response_model=AnalysisJobOut)
def create_analysis_job(
    document_id: UUID,
    payload: AnalysisJobCreate,
    db: Session = Depends(get_db),
):
    document = db.execute(select(Document).where(Document.id == document_id)).scalar_one_or_none()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found!")

    job = AnalysisJob(
        document_id=document_id,
        analysis_type=payload.analysis_type,
        status=AnalysisStatus.PENDING,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "id": str(job.id),
        "document_id": str(job.document_id),
        "analysis_type": job.analysis_type,
        "status": job.status,
        "created_at": job.created_at.isoformat(),
    }
