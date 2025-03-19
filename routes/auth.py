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
    print(user_info)  # Log the user_info to see what it contains

    # Check if email is present in user_info
    email = user_info["email"]
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not found in Google token"
        )

    first_name = user_info.get("given_name", "")
    last_name = user_info.get("family_name", "")
    picture = user_info.get("picture")
    
    if auth_request.user_type == "founder":
        result = await db.execute(
            text("SELECT * FROM founders WHERE email = :email"),
            {"email": email}
        )
        founder = result.first()
        
        if not founder:
            # Create new founder with required fields
            await db.execute(
                text("""
                    INSERT INTO founders (
                        email, first_name, last_name, gender, phone,
                        password_hashed, is_active, created_at
                    )
                    VALUES (
                        :email, :first_name, :last_name, 'Not Specified', 'Not Specified',
                        'google_auth', true, CURRENT_TIMESTAMP
                    )
                """),
                {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name
                }
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
            # Create new investor with required fields
            await db.execute(
                text("""
                    INSERT INTO investors (
                        email, first_name, last_name, gender, phone,
                        password_hashed, is_active, created_at
                    )
                    VALUES (
                        :email, :first_name, :last_name, 'Not Specified', 'Not Specified',
                        'google_auth', true, CURRENT_TIMESTAMP
                    )
                """),
                {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name
                }
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
        "name": f"{first_name} {last_name}",
        "picture": picture
    } 