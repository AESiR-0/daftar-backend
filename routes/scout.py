from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from schemas.scout import (
    ScoutCreate, ScoutResponse, ScoutDetailsUpdate, 
    ScoutAudienceUpdate, ScoutCollaborationUpdate,
    ScoutFAQCreate, ScoutFAQResponse,
    ScoutScheduleCreate, ScoutScheduleResponse,
    ScoutUpdateCreate, ScoutUpdateResponse
)
from typing import List, Optional

router = APIRouter(prefix="/scouts", tags=["scout"])

@router.post("/", response_model=ScoutResponse)
async def create_scout(
    scout_data: ScoutCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new scout with placeholder details"""
    result = await db.execute(
        text("""
            INSERT INTO scouts (daftar_id, name, status, created_at)
            VALUES (:daftar_id, :name, :status, CURRENT_TIMESTAMP)
            RETURNING *
        """),
        {
            "daftar_id": scout_data.daftar_id,
            "name": scout_data.name,
            "status": scout_data.status
        }
    )
    
    await db.commit()
    return result.first()

@router.put("/{scout_id}/details", response_model=ScoutResponse)
async def update_scout_details(
    scout_id: int,
    details: ScoutDetailsUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update scout name and vision"""
    result = await db.execute(
        text("""
            UPDATE scouts
            SET name = :name, vision = :vision
            WHERE id = :scout_id
            RETURNING *
        """),
        {
            "scout_id": scout_id,
            "name": details.name,
            "vision": details.vision
        }
    )
    
    await db.commit()
    return result.first()

@router.put("/{scout_id}/audience", response_model=ScoutResponse)
async def update_scout_audience(
    scout_id: int,
    audience: ScoutAudienceUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update scout audience details"""
    result = await db.execute(
        text("""
            UPDATE scouts
            SET location = :location,
                community = :community,
                age_range = :age_range,
                stage = :stage,
                sector = :sector
            WHERE id = :scout_id
            RETURNING *
        """),
        {
            "scout_id": scout_id,
            "location": audience.location,
            "community": audience.community,
            "age_range": audience.age_range,
            "stage": audience.stage,
            "sector": audience.sector
        }
    )
    
    await db.commit()
    return result.first()

@router.put("/{scout_id}/collaboration", response_model=ScoutResponse)
async def update_scout_collaboration(
    scout_id: int,
    collab: ScoutCollaborationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update scout collaboration details"""
    result = await db.execute(
        text("""
            UPDATE scouts
            SET team_size = :team_size,
                collaboration_type = :collaboration_type,
                collaboration_details = :collaboration_details
            WHERE id = :scout_id
            RETURNING *
        """),
        {
            "scout_id": scout_id,
            "team_size": collab.team_size,
            "collaboration_type": collab.collaboration_type,
            "collaboration_details": collab.collaboration_details
        }
    )
    
    await db.commit()
    return result.first()

@router.post("/{scout_id}/faqs", response_model=ScoutFAQResponse)
async def create_scout_faq(
    scout_id: int,
    faq: ScoutFAQCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add FAQ to scout"""
    result = await db.execute(
        text("""
            INSERT INTO scout_faqs (
                scout_id, question, answer, created_at
            )
            VALUES (
                :scout_id, :question, :answer, CURRENT_TIMESTAMP
            )
            RETURNING *
        """),
        {
            "scout_id": scout_id,
            "question": faq.question,
            "answer": faq.answer
        }
    )
    
    await db.commit()
    return result.first()

@router.get("/", response_model=List[ScoutResponse])
async def get_scouts(
    daftar_id: Optional[int] = None,  # Make daftar_id optional
    include_archived: bool = False,  # Optional parameter to include archived scouts
    db: AsyncSession = Depends(get_db)
):
    """Get all scouts, optionally filtered by daftar_id"""
    query = "SELECT * FROM scouts WHERE 1=1"  # Base query

    # Add condition for daftar_id if provided
    if daftar_id is not None:
        query += " AND daftar_id = :daftar_id"

    # Exclude archived scouts unless specified
    if not include_archived:
        query += " AND status != 'archived'"

    query += " ORDER BY created_at DESC"

    # Execute query with or without daftar_id
    result = await db.execute(
        text(query),
        {"daftar_id": daftar_id} if daftar_id is not None else {}
    )

    scouts = result.fetchall()
    return [dict(scout) for scout in scouts]

@router.post("/{scout_id}/schedule", response_model=ScoutScheduleResponse)
async def create_scout_schedule(
    scout_id: int,
    schedule: ScoutScheduleCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add schedule slot for scout"""
    result = await db.execute(
        text("""
            INSERT INTO scout_schedules (
                scout_id, date, time_slot, availability, created_at
            )
            VALUES (
                :scout_id, :date, :time_slot, :availability, CURRENT_TIMESTAMP
            )
            RETURNING *
        """),
        {
            "scout_id": scout_id,
            "date": schedule.date,
            "time_slot": schedule.time_slot,
            "availability": schedule.availability
        }
    )
    
    await db.commit()
    return result.first()

@router.put("/{scout_id}/submit", response_model=ScoutResponse)
async def submit_scout_for_approval(
    scout_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Submit scout for approval"""
    result = await db.execute(
        text("""
            UPDATE scouts
            SET status = 'pending'
            WHERE id = :scout_id AND status = 'draft'
            RETURNING *
        """),
        {"scout_id": scout_id}
    )
    
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scout must be in draft status to submit"
        )
    
    await db.commit()
    return result.first()

@router.put("/{scout_id}/approve", response_model=ScoutResponse)
async def approve_scout(
    scout_id: int,
    approver_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Approve a scout"""
    result = await db.execute(
        text("""
            UPDATE scouts
            SET status = 'approved',
                approved_at = CURRENT_TIMESTAMP,
                approved_by = :approver_id
            WHERE id = :scout_id AND status = 'pending'
            RETURNING *
        """),
        {
            "scout_id": scout_id,
            "approver_id": approver_id
        }
    )
    
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scout must be in pending status to approve"
        )
    
    await db.commit()
    return result.first()

@router.post("/{scout_id}/updates", response_model=ScoutUpdateResponse)
async def create_scout_update(
    scout_id: int,
    update: ScoutUpdateCreate,
    creator_id: int,  # This would typically come from auth token
    db: AsyncSession = Depends(get_db)
):
    """Create a new update for a scout"""
    # First verify the scout exists
    scout_check = await db.execute(
        text("SELECT id FROM scouts WHERE id = :scout_id"),
        {"scout_id": scout_id}
    )
    if not scout_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found"
        )
    
    # Create update
    result = await db.execute(
        text("""
            INSERT INTO scout_updates (
                scout_id, description, created_at, created_by
            )
            VALUES (
                :scout_id, :description, CURRENT_TIMESTAMP, :creator_id
            )
            RETURNING *
        """),
        {
            "scout_id": scout_id,
            "description": update.description,
            "creator_id": creator_id
        }
    )
    
    await db.commit()
    return result.first()

@router.get("/{scout_id}/updates", response_model=List[ScoutUpdateResponse])
async def get_scout_updates(
    scout_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all updates for a scout"""
    # First verify the scout exists
    scout_check = await db.execute(
        text("SELECT id FROM scouts WHERE id = :scout_id"),
        {"scout_id": scout_id}
    )
    if not scout_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found"
        )
    
    # Get updates
    result = await db.execute(
        text("""
            SELECT * FROM scout_updates
            WHERE scout_id = :scout_id
            ORDER BY created_at DESC
        """),
        {"scout_id": scout_id}
    )
    
    updates = result.fetchall()
    return [dict(update) for update in updates]

@router.get("/{scout_id}/faqs", response_model=List[ScoutFAQResponse])
async def get_scout_faqs(
    scout_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all FAQs for a scout"""
    # First verify scout exists and is not archived
    scout_check = await db.execute(
        text("""
            SELECT id FROM scouts 
            WHERE id = :scout_id 
            AND status != 'archived'
        """),
        {"scout_id": scout_id}
    )
    
    if not scout_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found or is archived"
        )
    
    result = await db.execute(
        text("""
            SELECT * FROM scout_faqs
            WHERE scout_id = :scout_id
            ORDER BY created_at DESC
        """),
        {"scout_id": scout_id}
    )
    
    return result.fetchall()

@router.put("/{scout_id}/archive", response_model=ScoutResponse)
async def archive_scout(
    scout_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Archive a scout"""
    # First verify the scout exists and isn't already archived
    scout_check = await db.execute(
        text("""
            SELECT id, status 
            FROM scouts 
            WHERE id = :scout_id
        """),
        {"scout_id": scout_id}
    )
    scout = scout_check.first()
    
    if not scout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found"
        )
    
    if scout.status == 'archived':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scout is already archived"
        )
    
    # Archive the scout
    result = await db.execute(
        text("""
            UPDATE scouts
            SET status = 'archived'
            WHERE id = :scout_id
            RETURNING *
        """),
        {"scout_id": scout_id}
    )
    
    await db.commit()
    return result.first() 