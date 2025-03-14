from pydantic import BaseModel

class GoogleAuthRequest(BaseModel):
    token: str
    user_type: str  # 'founder' or 'investor'

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_type: str
    email: str
    name: str
    picture: str | None 