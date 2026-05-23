"""Pydantic schemas for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class DateSourceEnum(str, Enum):
    """Sources for extracted dates."""
    EXIF = "exif"
    PDF_METADATA = "pdf_metadata"
    FILENAME = "filename"
    OCR = "ocr"
    FILE_METADATA = "file_metadata"
    MANUAL = "manual"


class SourceDocumentResponse(BaseModel):
    """Response model for source documents."""
    id: str
    packet_id: str
    original_filename: str
    file_type: str
    file_size: int
    upload_date: datetime
    extracted_date: Optional[datetime]
    date_confidence: float
    date_source: Optional[DateSourceEnum]
    
    class Config:
        from_attributes = True


class SourceDocumentCreate(BaseModel):
    """Request model for creating source documents."""
    packet_id: str
    original_filename: str
    file_type: str
    file_size: int


class DateExtractionResult(BaseModel):
    """Result of date extraction."""
    date: Optional[datetime]
    source: DateSourceEnum
    confidence: float
    filename: str
    
    class Config:
        from_attributes = True


class FileUploadResponse(BaseModel):
    """Response for file upload."""
    id: str
    original_filename: str
    file_type: str
    file_size: int
    upload_date: datetime
    extracted_date: Optional[datetime]
    date_confidence: float
    date_source: Optional[str]
    message: str


class PacketCreate(BaseModel):
    """Request model for creating packets."""
    name: str
    description: Optional[str] = None
    case_number: Optional[str] = None
    jurisdiction: Optional[str] = None


class PacketResponse(BaseModel):
    """Response model for packets."""
    id: str
    name: str
    description: Optional[str]
    case_number: Optional[str]
    jurisdiction: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    source_document_count: int = 0
    
    class Config:
        from_attributes = True
