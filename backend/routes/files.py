"""File upload and processing routes."""

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from typing import List

router = APIRouter()


@router.post("/upload")
async def upload_files(
    packet_id: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload multiple files for a packet.
    
    - **packet_id**: ID of the packet to add files to
    - **files**: List of files to upload
    """
    # TODO: Implement file upload logic
    return {"message": "Files uploaded", "file_count": len(files)}


@router.get("/")
async def list_files(packet_id: str, db: Session = Depends(get_db)):
    """
    List all files in a packet.
    """
    # TODO: Implement file listing
    return {"files": []}
