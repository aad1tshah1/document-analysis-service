from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.db.session import get_db
from app.db.models import AnalysisJob, AnalysisStatus, AnalysisType
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(prefix="/analysis-jobs", tags=["analysis-jobs"])

class AnalysisJobOut(BaseModel):
    id: str
    document_id: str
    analysis_type: AnalysisType
    status: AnalysisStatus
    result: dict | None
    model: str | None
    error: str | None
    created_at: str
    started_at: str | None
    completed_at: str | None

@router.get("/{job_id}", response_model=AnalysisJobOut)
def get_analysis_job(job_id: UUID, db:Session = Depends(get_db)):
    statement = select(AnalysisJob).where(AnalysisJob.id == job_id)
    job = db.execute(statement).scalar_one_or_none()

    if job is None:
        raise HTTPException(status_code=404, detail="Analyis Job not found")
    
    return {
        "id": str(job.id),
        "document_id": str(job.document_id),
        "analysis_type": job.analysis_type,
        "status": job.status,
        "result": job.result,
        "model": job.model,
        "error": job.error,
        "created_at": job.created_at.isoformat(),
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None
        }



