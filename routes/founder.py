from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from schemas.founder import FounderProfileResponse, InvestorQuestionResponse, QuestionAnswerResponse
from typing import List
from schemas.pitch import PitchResponse
from schemas.document import DocumentCreate, DocumentResponse

router = APIRouter(prefix="/founder", tags=["founder"])

@router.get("/profile/{founder_id}", response_model=FounderProfileResponse)
async def get_founder_profile(
    founder_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get founder profile details by ID"""
    founder = await db.execute(
        text("""
            SELECT * FROM founders WHERE id = :founder_id AND is_active = true AND deleted_on IS NULL
        """),
        {"founder_id": founder_id}
    )
    result = founder.first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Founder not found"
        )
        
    return result

@router.get("/{founder_id}/pitches", response_model=List[PitchResponse])
async def get_founder_pitches(
    founder_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all pitches for a founder"""
    # First check if founder exists
    founder_query = await db.execute(
        text("SELECT id FROM founders WHERE id = :founder_id"),
        {"founder_id": founder_id}
    )
    founder = founder_query.first()
    
    if not founder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Founder not found"
        )
    
    # Get all pitches for this founder through the relationship table
    result = await db.execute(
        text("""
            SELECT p.* 
            FROM pitches p
            JOIN founder_pitch_relationship fpr ON p.id = fpr.pitch_id
            WHERE fpr.founder_id = :founder_id
            ORDER BY p.created_at DESC
        """),
        {"founder_id": founder_id}
    )
    
    pitches = result.fetchall()
    return [dict(pitch) for pitch in pitches]

@router.get("/{founder_id}/pitches/{pitch_id}/questions", response_model=List[QuestionAnswerResponse])
async def get_founder_pitch_questions(
    founder_id: int,
    pitch_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all investor questions and answers for a founder's pitch"""
    # First verify the founder exists and has access to this pitch
    access_check = await db.execute(
        text("""
            SELECT 1 FROM founder_pitch_relationship
            WHERE founder_id = :founder_id 
            AND pitch_id = :pitch_id
        """),
        {
            "founder_id": founder_id,
            "pitch_id": pitch_id
        }
    )
    
    if not access_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found or founder does not have access"
        )
    
    # Get all questions and their answers
    result = await db.execute(
        text("""
            SELECT 
                q.id as question_id,
                q.question_text,
                a.video_url as answer_video_url,
                a.answer_text,
                a.answered_at
            FROM investor_questions q
            LEFT JOIN question_answers a ON q.id = a.question_id
            WHERE q.pitch_id = :pitch_id
            ORDER BY q.created_at DESC
        """),
        {"pitch_id": pitch_id}
    )
    
    questions = result.fetchall()
    return [dict(q) for q in questions]

@router.get("/{founder_id}/questions/unanswered", response_model=List[QuestionAnswerResponse])
async def get_founder_unanswered_questions(
    founder_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all unanswered questions across all pitches for a founder"""
    # Get all unanswered questions from all founder's pitches
    result = await db.execute(
        text("""
            SELECT 
                q.id as question_id,
                q.question_text,
                NULL as answer_video_url,
                NULL as answer_text,
                NULL as answered_at
            FROM investor_questions q
            JOIN founder_pitch_relationship fpr ON q.pitch_id = fpr.pitch_id
            LEFT JOIN question_answers a ON q.id = a.question_id
            WHERE fpr.founder_id = :founder_id
            AND a.id IS NULL
            ORDER BY q.created_at DESC
        """),
        {"founder_id": founder_id}
    )
    
    questions = result.fetchall()
    return [dict(q) for q in questions]

@router.post("/{founder_id}/pitches/{pitch_id}/documents", response_model=DocumentResponse)
async def upload_founder_document(
    founder_id: int,
    pitch_id: int,
    document: DocumentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Upload a document to a pitch as a founder"""
    # Verify founder has access to this pitch
    access_check = await db.execute(
        text("""
            SELECT 1 FROM founder_pitch_relationship
            WHERE founder_id = :founder_id 
            AND pitch_id = :pitch_id
        """),
        {
            "founder_id": founder_id,
            "pitch_id": pitch_id
        }
    )
    
    if not access_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found or founder does not have access"
        )
    
    # Create document
    result = await db.execute(
        text("""
            INSERT INTO documents (
                pitch_id, document_url, document_type, title,
                description, is_private, uploaded_by_type,
                uploaded_by_id, uploaded_at
            )
            VALUES (
                :pitch_id, :document_url, :document_type, :title,
                :description, :is_private, 'founder',
                :founder_id, CURRENT_TIMESTAMP
            )
            RETURNING *
        """),
        {
            "pitch_id": pitch_id,
            "document_url": document.document_url,
            "document_type": document.document_type,
            "title": document.title,
            "description": document.description,
            "is_private": document.is_private,
            "founder_id": founder_id
        }
    )
    
    await db.commit()
    return result.first()

@router.get("/{founder_id}/pitches/{pitch_id}/documents", response_model=List[DocumentResponse])
async def get_founder_pitch_documents(
    founder_id: int,
    pitch_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all accessible documents for a pitch"""
    # Verify founder has access to this pitch
    access_check = await db.execute(
        text("""
            SELECT 1 FROM founder_pitch_relationship
            WHERE founder_id = :founder_id 
            AND pitch_id = :pitch_id
        """),
        {
            "founder_id": founder_id,
            "pitch_id": pitch_id
        }
    )
    
    if not access_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found or founder does not have access"
        )
    
    # Get documents
    # Founders can see all their own documents plus non-private investor documents
    result = await db.execute(
        text("""
            SELECT * FROM documents
            WHERE pitch_id = :pitch_id
            AND (
                (uploaded_by_type = 'founder' AND uploaded_by_id = :founder_id)
                OR
                (uploaded_by_type = 'investor' AND is_private = false)
            )
            ORDER BY uploaded_at DESC
        """),
        {
            "pitch_id": pitch_id,
            "founder_id": founder_id
        }
    )
    
    documents = result.fetchall()
    return [dict(doc) for doc in documents] 