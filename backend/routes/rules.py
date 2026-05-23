"""Legal rules management routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


@router.get("/states")
async def list_states(db: Session = Depends(get_db)):
    """
    List available states with legal rules.
    """
    # TODO: Return list of states
    return {"states": []}


@router.get("/by-state/{state}")
async def get_rules_by_state(state: str, db: Session = Depends(get_db)):
    """
    Get all legal rules for a specific state.
    """
    # TODO: Implement rule retrieval
    return {"state": state, "rules": []}
