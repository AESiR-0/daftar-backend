from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from schemas.daftar import DaftarCreate, DaftarResponse
from typing import List

router = APIRouter(prefix="/daftars", tags=["daftar"])

@router.post("/", response_model=DaftarResponse)
async def create_daftar(
    daftar_data: DaftarCreate,
    investor_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Create a new daftar using an investor ID"""
    # Verify the investor exists
    investor_check = await db.execute(
        text("SELECT id FROM investors WHERE id = :investor_id"),
        {"investor_id": investor_id}
    )
    if not investor_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investor not found"
        )
    
    # Create the new daftar
    result = await db.execute(
        text("""
            INSERT INTO daftars (
                name, type, daftar_code, website, location, big_picture,
                on_daftar_since, billing_plan, billing_information, is_active
            )
            VALUES (
                :name, :type, :daftar_code, :website, :location, :big_picture,
                CURRENT_TIMESTAMP, :billing_plan, :billing_information, true
            )
            RETURNING *
        """),
        {
            "name": daftar_data.name,
            "type": daftar_data.type,
            "daftar_code": daftar_data.daftar_code,
            "website": daftar_data.website,
            "location": daftar_data.location,
            "big_picture": daftar_data.big_picture,
            "billing_plan": daftar_data.billing_plan,
            "billing_information": daftar_data.billing_information
        }
    )
    
    await db.commit()
    return result.first()

@router.post("/join", response_model=DaftarResponse)
async def join_daftar(
    daftar_code: str,
    investor_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Join a daftar using a daftar code"""
    # Verify the daftar exists
    daftar_check = await db.execute(
        text("SELECT id FROM daftars WHERE daftar_code = :daftar_code AND is_active = true"),
        {"daftar_code": daftar_code}
    )
    daftar = daftar_check.first()
    
    if not daftar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daftar not found or is not active"
        )
    
    # Check if the investor is already a member of the daftar
    membership_check = await db.execute(
        text("""
            SELECT 1 FROM daftar_investors
            WHERE daftar_id = :daftar_id AND investor_id = :investor_id
        """),
        {"daftar_id": daftar.id, "investor_id": investor_id}
    )
    
    if membership_check.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Investor is already a member of this daftar"
        )
    
    # Add the investor to the daftar
    await db.execute(
        text("""
            INSERT INTO daftar_investors (daftar_id, investor_id, role, joined_at, is_active)
            VALUES (:daftar_id, :investor_id, 'member', CURRENT_TIMESTAMP, true)
        """),
        {"daftar_id": daftar.id, "investor_id": investor_id}
    )
    
    await db.commit()
    return daftar 