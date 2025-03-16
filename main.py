from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from routes import founder, investor, scout, auth, pitch
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import text

logger = logging.getLogger(__name__)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     try:
#         # Setup
#         await init_db()
#         logger.info("Database initialized successfully")
#     except Exception as e:
#         logger.error(f"Failed to initialize database: {str(e)}")
#         raise
#     yield
#     # # Cleanup (if needed)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(founder.router)
app.include_router(investor.router)
app.include_router(scout.router)
app.include_router(pitch.router)

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    """Health check endpoint"""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return {"status": "unhealthy", "error": 'Database connection error'}


