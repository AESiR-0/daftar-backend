from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from schemas.scout import ScoutPitchResponse
from typing import List
from fastapi import status

router = APIRouter(prefix="/scouts", tags=["scout"])

@router.get("/{scout_id}/pitches", response_model=List[ScoutPitchResponse])
async def get_scout_pitches(
    scout_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all pitches for a scout"""
    # First check if scout exists
    scout_query = await db.execute(
        text("SELECT id FROM scouts WHERE id = :scout_id"),
        {"scout_id": scout_id}
    )
    scout = scout_query.first()
    
    if not scout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found"
        )
    
    # Get all pitches and their associated founders for this scout
    result = await db.execute(
        text("""
            SELECT 
                p.*,
                f.id as founder_id,
                f.first_name,
                f.last_name,
                f.phone
            FROM pitches p
            LEFT JOIN founder_pitch_relationship fpr ON p.id = fpr.pitch_id
            LEFT JOIN founders f ON fpr.founder_id = f.id
            WHERE p.scout_id = :scout_id
            ORDER BY p.created_at DESC
        """),
        {"scout_id": scout_id}
    )
    
    rows = result.fetchall()
    
    if not rows:
        return []
    
    # Group pitches with their founders
    pitches_dict = {}
    for row in rows:
        pitch_id = row.id
        if pitch_id not in pitches_dict:
            pitches_dict[pitch_id] = {
                "id": row.id,
                "pitch_name": row.pitch_name,
                "investor_question_language": row.investor_question_language,
                "ask_for_investor": row.ask_for_investor,
                "has_confirmed": row.has_confirmed,
                "created_at": row.created_at,
                "founders": []
            }
        
        if row.founder_id:  # Only add founder if exists
            founder = {
                "id": row.founder_id,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "phone": row.phone
            }
            pitches_dict[pitch_id]["founders"].append(founder)
    
    return list(pitches_dict.values()) 