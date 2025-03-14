from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from schemas.pitch import PitchResponse, PitchCreate, PitchUpdate
from schemas.invite import DaftarInviteResponse, DaftarInviteCreate, PitchTeamInviteResponse, PitchTeamInviteCreate
from typing import List

router = APIRouter(prefix="/pitches", tags=["pitch"])

@router.post("/", response_model=PitchResponse)
async def create_pitch(
    pitch_data: PitchCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new pitch"""
    # Check if scout exists
    scout_query = await db.execute(
        text("SELECT id FROM scouts WHERE id = :scout_id"),
        {"scout_id": pitch_data.scout_id}
    )
    if not scout_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found"
        )
    
    # Create new pitch
    result = await db.execute(
        text("""
            INSERT INTO pitches (
                pitch_name, scout_id, founder_language,
                ask_for_investor, has_confirmed, status_founder,
                demo_link, created_at
            )
            VALUES (
                :pitch_name, :scout_id, :founder_language,
                :ask_for_investor, false, 'Inbox',
                :demo_link, CURRENT_TIMESTAMP
            )
            RETURNING *
        """),
        {
            "pitch_name": pitch_data.pitch_name,
            "scout_id": pitch_data.scout_id,
            "founder_language": pitch_data.founder_language,
            "ask_for_investor": pitch_data.ask_for_investor,
            "demo_link": pitch_data.demo_link
        }
    )
    
    new_pitch = result.first()
    await db.commit()
    return new_pitch

@router.get("/{pitch_id}", response_model=PitchResponse)
async def get_pitch(
    pitch_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get pitch details by ID"""
    pitch = await db.execute(
        text("SELECT * FROM pitches WHERE id = :pitch_id"),
        {"pitch_id": pitch_id}
    )
    result = pitch.first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found"
        )
        
    return result

@router.patch("/{pitch_id}", response_model=PitchResponse)
async def update_pitch(
    pitch_id: int,
    pitch_data: PitchUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update pitch details"""
    # Check if pitch exists
    pitch_query = await db.execute(
        text("SELECT id FROM pitches WHERE id = :pitch_id"),
        {"pitch_id": pitch_id}
    )
    if not pitch_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found"
        )
    
    # Build update query dynamically based on provided fields
    update_fields = {}
    update_query_parts = []
    
    if pitch_data.pitch_name is not None:
        update_fields["pitch_name"] = pitch_data.pitch_name
        update_query_parts.append("pitch_name = :pitch_name")
        
    if pitch_data.founder_language is not None:
        update_fields["founder_language"] = pitch_data.founder_language
        update_query_parts.append("founder_language = :founder_language")
        
    if pitch_data.ask_for_investor is not None:
        update_fields["ask_for_investor"] = pitch_data.ask_for_investor
        update_query_parts.append("ask_for_investor = :ask_for_investor")
        
    if pitch_data.has_confirmed is not None:
        update_fields["has_confirmed"] = pitch_data.has_confirmed
        update_query_parts.append("has_confirmed = :has_confirmed")
        
    if pitch_data.status_founder is not None:
        update_fields["status_founder"] = pitch_data.status_founder
        update_query_parts.append("status_founder = :status_founder")
        
    if pitch_data.demo_link is not None:
        update_fields["demo_link"] = pitch_data.demo_link
        update_query_parts.append("demo_link = :demo_link")
    
    if not update_fields:
        return await get_pitch(pitch_id, db)
    
    # Add pitch_id to update fields
    update_fields["pitch_id"] = pitch_id
    
    # Execute update query
    result = await db.execute(
        text(f"""
            UPDATE pitches
            SET {", ".join(update_query_parts)}
            WHERE id = :pitch_id
            RETURNING *
        """),
        update_fields
    )
    
    await db.commit()
    return result.first()

@router.delete("/{pitch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pitch(
    pitch_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a pitch"""
    # Check if pitch exists
    pitch_query = await db.execute(
        text("SELECT id FROM pitches WHERE id = :pitch_id"),
        {"pitch_id": pitch_id}
    )
    if not pitch_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found"
        )
    
    # Delete pitch
    await db.execute(
        text("DELETE FROM pitches WHERE id = :pitch_id"),
        {"pitch_id": pitch_id}
    )
    await db.commit()

@router.post("/{pitch_id}/team/invite", response_model=PitchTeamInviteResponse)
async def invite_team_member(
    pitch_id: int,
    invite_data: PitchTeamInviteCreate,
    db: AsyncSession = Depends(get_db)
):
    """Invite a member to pitch team"""
    # Check if pitch exists
    pitch_query = await db.execute(
        text("SELECT id FROM pitches WHERE id = :pitch_id"),
        {"pitch_id": pitch_id}
    )
    if not pitch_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found"
        )
    
    # Check if invite already exists
    existing_invite = await db.execute(
        text("""
            SELECT id FROM pitch_team_invites 
            WHERE pitch_id = :pitch_id 
            AND invited_email = :email 
            AND status = 'pending'
        """),
        {
            "pitch_id": pitch_id,
            "email": invite_data.invited_email
        }
    )
    if existing_invite.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invite already sent to this email"
        )
    
    # Create invite
    result = await db.execute(
        text("""
            INSERT INTO pitch_team_invites (
                pitch_id, invited_email, first_name, last_name,
                designation, role, status, created_at
            )
            VALUES (
                :pitch_id, :email, :first_name, :last_name,
                :designation, :role, 'pending', CURRENT_TIMESTAMP
            )
            RETURNING *
        """),
        {
            "pitch_id": pitch_id,
            "email": invite_data.invited_email,
            "first_name": invite_data.first_name,
            "last_name": invite_data.last_name,
            "designation": invite_data.designation,
            "role": invite_data.role
        }
    )
    
    await db.commit()
    return result.first() 