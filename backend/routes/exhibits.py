"""Exhibit management routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


@router.get("/")
async def list_exhibits(packet_id: str, db: Session = Depends(get_db)):
    """
    List all exhibits in a packet.
    """
    # TODO: Implement exhibit listing
    return {"exhibits": []}


@router.post("/organize")
async def organize_exhibits(packet_id: str, db: Session = Depends(get_db)):
    """
    Auto-organize exhibits from source documents in chronological order.
    """
    # TODO: Implement auto-organization
    return {"message": "Exhibits organized"}
