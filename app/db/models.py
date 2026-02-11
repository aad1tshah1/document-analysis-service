import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class AnalysisStatus(str, enum.Enum):
    """
    Status of Analysis
    """
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AnalysisType(str,enum.Enum):
    """
    Type of Analysis
    """
    SUMMARY="SUMMARY"
    

class Document(Base):
    """
    Generating Document Table
    """
    __tablename__ = "documents"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title:Mapped[str] = mapped_column(String(300))
    description:Mapped[str] = mapped_column(String(300))
    content:Mapped[str] = mapped_column(Text)

    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    analysis_jobs: Mapped[list["AnalysisJob"]] = relationship(back_populates="document")


class AnalysisJob(Base):
    """
    Analysis Job
    """
    __tablename__ = "analysis_jobs"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    
    analysis_type:Mapped[AnalysisType] = mapped_column(Enum(AnalysisType), nullable=False)
    status:Mapped[AnalysisStatus] = mapped_column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING, index=True)

    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    model: Mapped[str | None] = mapped_column(String(80), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    document: Mapped[Document] = relationship(back_populates="analysis_jobs")

