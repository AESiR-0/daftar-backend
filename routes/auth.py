from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.auth import GoogleAuthRequest
from auth import verify_google_token, create_access_token
from sqlalchemy import text
from datetime import datetime, timedelta

router = APIRouter(tags=["auth"])

@router.post("/auth/login")
async def login(auth_request: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):
    """Handle Google OAuth login"""
    # Verify the Google token
    user_info = verify_google_token(auth_request.token)
    
    # Extract user information
    email = user_info["email"]
    name = user_info.get("name")
    picture = user_info.get("picture")
    
    if auth_request.user_type == "founder":
        result = await db.execute(
            text("SELECT * FROM founders WHERE email = :email"),
            {"email": email}
        )
        founder = result.first()
        
        if not founder:
            # Create new founder
            await db.execute(
                text("""
                    INSERT INTO founders (email, name, created_at, updated_at)
                    VALUES (:email, :name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """),
                {"email": email, "name": name}
            )
            await db.commit()
        
        # Create JWT token with founder role
        access_token = create_access_token(
            data={"sub": email, "role": "founder"},
            expires_delta=timedelta(minutes=30)
        )
        
    elif auth_request.user_type == "investor":
        result = await db.execute(
            text("SELECT * FROM investors WHERE email = :email"),
            {"email": email}
        )
        investor = result.first()
        
        if not investor:
            # Create new investor
            await db.execute(
                text("""
                    INSERT INTO investors (email, name, created_at, updated_at)
                    VALUES (:email, :name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """),
                {"email": email, "name": name}
            )
            await db.commit()
        
        # Create JWT token with investor role
        access_token = create_access_token(
            data={"sub": email, "role": "investor"},
            expires_delta=timedelta(minutes=30)
        )
        
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user type. Must be 'founder' or 'investor'"
        )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": auth_request.user_type,
        "email": email,
        "name": name,
        "picture": picture
    } 