from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from schemas.investor import InvestorProfileResponse, DaftarProfileResponse, DaftarInvestorResponse, DaftarInvestorCreate, SampleQuestionResponse, CustomQuestionCreate, CustomQuestionResponse
from typing import List, Optional
from schemas.document import DocumentCreate, DocumentResponse
from schemas.offer import OfferCreate, OfferResponse, OfferActionCreate
from schemas.bill import BillCreate, BillResponse

router = APIRouter(tags=["investor"])

@router.get("/investor/profile/{investor_id}", response_model=InvestorProfileResponse)
async def get_investor_profile(
    investor_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get investor profile details by ID"""
    investor = await db.execute(
        text("""
            SELECT * FROM investors WHERE id = :investor_id AND is_active = true
        """),
        {"investor_id": investor_id}
    )
    result = investor.first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investor not found"
        )
        
    return result

@router.get("/daftar/profile/{daftar_id}", response_model=DaftarProfileResponse)
async def get_daftar_profile(
    daftar_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get daftar profile details by ID"""
    daftar = await db.execute(
        text("""
            SELECT * FROM daftars WHERE id = :daftar_id AND is_active = true
        """),
        {"daftar_id": daftar_id}
    )
    result = daftar.first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daftar not found"
        )
        
    return result

@router.get("/daftars/{daftar_id}/investors", response_model=List[DaftarInvestorResponse])
async def get_daftar_investors(
    daftar_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all investors in a daftar"""
    # Check if daftar exists
    daftar_query = await db.execute(
        text("SELECT id FROM daftars WHERE id = :daftar_id"),
        {"daftar_id": daftar_id}
    )
    if not daftar_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daftar not found"
        )
    
    # Get all active investors for this daftar
    result = await db.execute(
        text("""
            SELECT 
                di.id,
                di.investor_id,
                i.first_name,
                i.last_name,
                di.role,
                di.joined_at,
                di.is_active
            FROM daftar_investors di
            JOIN investors i ON di.investor_id = i.id
            WHERE di.daftar_id = :daftar_id AND di.is_active = true
            ORDER BY di.joined_at DESC
        """),
        {"daftar_id": daftar_id}
    )
    
    investors = result.fetchall()
    return [dict(investor) for investor in investors]

@router.post("/daftars/{daftar_id}/investors", response_model=DaftarInvestorResponse)
async def add_investor_to_daftar(
    daftar_id: int,
    investor_data: DaftarInvestorCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add an investor to a daftar"""
    # Check if daftar exists and is active
    daftar_query = await db.execute(
        text("SELECT id, is_active FROM daftars WHERE id = :daftar_id"),
        {"daftar_id": daftar_id}
    )
    daftar = daftar_query.first()
    
    if not daftar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daftar not found"
        )
    
    if not daftar.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This daftar is not active"
        )
    
    # Check if investor exists
    investor_query = await db.execute(
        text("SELECT id FROM investors WHERE id = :investor_id"),
        {"investor_id": investor_data.investor_id}
    )
    investor = investor_query.first()
    
    if not investor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investor not found"
        )
    
    # Check if relationship already exists
    existing_query = await db.execute(
        text("""
            SELECT id FROM daftar_investors 
            WHERE daftar_id = :daftar_id AND investor_id = :investor_id AND is_active = true
        """),
        {"daftar_id": daftar_id, "investor_id": investor_data.investor_id}
    )
    
    if existing_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Investor is already a member of this daftar"
        )
    
    # Create new daftar-investor relationship
    result = await db.execute(
        text("""
            INSERT INTO daftar_investors (daftar_id, investor_id, role, joined_at, is_active)
            VALUES (:daftar_id, :investor_id, :role, CURRENT_TIMESTAMP, true)
            RETURNING id, joined_at
        """),
        {
            "daftar_id": daftar_id,
            "investor_id": investor_data.investor_id,
            "role": investor_data.role
        }
    )
    
    new_relationship = result.first()
    await db.commit()
    
    # Get investor details
    investor_details = await db.execute(
        text("""
            SELECT i.first_name, i.last_name
            FROM investors i
            WHERE i.id = :investor_id
        """),
        {"investor_id": investor_data.investor_id}
    )
    investor_info = investor_details.first()
    
    return {
        "id": new_relationship.id,
        "investor_id": investor_data.investor_id,
        "first_name": investor_info.first_name,
        "last_name": investor_info.last_name,
        "role": investor_data.role,
        "joined_at": new_relationship.joined_at,
        "is_active": True
    }

@router.get("/scouts/{scout_id}/sample-questions", response_model=List[SampleQuestionResponse])
async def get_sample_questions(
    scout_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all sample questions and answers for a scout"""
    # Check if scout exists
    scout_query = await db.execute(
        text("SELECT id FROM scouts WHERE id = :scout_id"),
        {"scout_id": scout_id}
    )
    if not scout_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found"
        )
    
    # Get sample questions with their answers
    result = await db.execute(
        text("""
            SELECT 
                q.id,
                q.scout_id,
                q.question_text,
                a.video_url
            FROM sample_investor_questions q
            LEFT JOIN sample_pitch_answers a ON q.id = a.question_id
            WHERE q.scout_id = :scout_id
            ORDER BY q.id
        """),
        {"scout_id": scout_id}
    )
    
    questions = result.fetchall()
    return [dict(q) for q in questions]

@router.post("/scouts/{scout_id}/custom-questions", response_model=CustomQuestionResponse)
async def create_custom_question(
    scout_id: int,
    question_data: CustomQuestionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a custom question for a scout"""
    # Check if scout exists
    scout_query = await db.execute(
        text("SELECT id FROM scouts WHERE id = :scout_id"),
        {"scout_id": scout_id}
    )
    if not scout_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found"
        )
    
    # Create custom question
    result = await db.execute(
        text("""
            INSERT INTO custom_investor_questions (
                scout_id, question_text, created_at
            )
            VALUES (
                :scout_id, :question_text, CURRENT_TIMESTAMP
            )
            RETURNING *
        """),
        {
            "scout_id": scout_id,
            "question_text": question_data.question_text
        }
    )
    
    await db.commit()
    return result.first()

@router.get("/scouts/{scout_id}/custom-questions", response_model=List[CustomQuestionResponse])
async def get_custom_questions(
    scout_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all custom questions for a scout"""
    # Check if scout exists
    scout_query = await db.execute(
        text("SELECT id FROM scouts WHERE id = :scout_id"),
        {"scout_id": scout_id}
    )
    if not scout_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scout not found"
        )
    
    # Get custom questions
    result = await db.execute(
        text("""
            SELECT * FROM custom_investor_questions
            WHERE scout_id = :scout_id
            ORDER BY created_at DESC
        """),
        {"scout_id": scout_id}
    )
    
    questions = result.fetchall()
    return [dict(q) for q in questions]

@router.post("/pitches/{pitch_id}/questions/{question_id}/answers")
async def create_question_answer(
    pitch_id: int,
    question_id: int,
    answer_text: Optional[str] = None,
    video_url: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create an answer for a question"""
    # Validate that either answer_text or video_url is provided
    if not answer_text and not video_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either answer_text or video_url must be provided"
        )
    
    # Check if question exists and belongs to this pitch
    question_query = await db.execute(
        text("""
            SELECT id FROM investor_questions 
            WHERE id = :question_id AND pitch_id = :pitch_id
        """),
        {
            "question_id": question_id,
            "pitch_id": pitch_id
        }
    )
    if not question_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found for this pitch"
        )
    
    # Check if answer already exists
    existing_answer = await db.execute(
        text("SELECT id FROM question_answers WHERE question_id = :question_id"),
        {"question_id": question_id}
    )
    if existing_answer.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Answer already exists for this question"
        )
    
    # Create answer
    result = await db.execute(
        text("""
            INSERT INTO question_answers (
                question_id, answer_text, video_url, answered_at
            )
            VALUES (
                :question_id, :answer_text, :video_url, CURRENT_TIMESTAMP
            )
            RETURNING *
        """),
        {
            "question_id": question_id,
            "answer_text": answer_text,
            "video_url": video_url
        }
    )
    
    await db.commit()
    return {"status": "success", "message": "Answer created successfully"}

@router.post("/pitches/{pitch_id}/documents", response_model=DocumentResponse)
async def upload_investor_document(
    pitch_id: int,
    investor_id: int,
    document: DocumentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Upload a document to a pitch as an investor"""
    # Verify investor has access to this pitch (through scout/daftar)
    access_check = await db.execute(
        text("""
            SELECT 1 FROM pitches p
            JOIN scouts s ON p.scout_id = s.id
            JOIN daftar_investors di ON s.daftar_id = di.daftar_id
            WHERE p.id = :pitch_id 
            AND di.investor_id = :investor_id
            AND di.is_active = true
        """),
        {
            "pitch_id": pitch_id,
            "investor_id": investor_id
        }
    )
    
    if not access_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found or investor does not have access"
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
                :description, :is_private, 'investor',
                :investor_id, CURRENT_TIMESTAMP
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
            "investor_id": investor_id
        }
    )
    
    await db.commit()
    return result.first()

@router.get("/pitches/{pitch_id}/documents", response_model=List[DocumentResponse])
async def get_investor_pitch_documents(
    pitch_id: int,
    investor_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all accessible documents for a pitch"""
    # Verify investor has access to this pitch
    access_check = await db.execute(
        text("""
            SELECT 1 FROM pitches p
            JOIN scouts s ON p.scout_id = s.id
            JOIN daftar_investors di ON s.daftar_id = di.daftar_id
            WHERE p.id = :pitch_id 
            AND di.investor_id = :investor_id
            AND di.is_active = true
        """),
        {
            "pitch_id": pitch_id,
            "investor_id": investor_id
        }
    )
    
    if not access_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found or investor does not have access"
        )
    
    # Get documents
    # Investors can see all their own documents plus non-private founder documents
    result = await db.execute(
        text("""
            SELECT * FROM documents
            WHERE pitch_id = :pitch_id
            AND (
                (uploaded_by_type = 'investor' AND uploaded_by_id = :investor_id)
                OR
                (uploaded_by_type = 'founder' AND is_private = false)
            )
            ORDER BY uploaded_at DESC
        """),
        {
            "pitch_id": pitch_id,
            "investor_id": investor_id
        }
    )
    
    documents = result.fetchall()
    return [dict(doc) for doc in documents]

@router.post("/pitches/{pitch_id}/offers", response_model=OfferResponse)
async def create_offer(
    pitch_id: int,
    investor_id: int,
    offer: OfferCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new offer for a pitch"""
    # Verify investor has access to this pitch
    access_check = await db.execute(
        text("""
            SELECT 1 FROM pitches p
            JOIN scouts s ON p.scout_id = s.id
            JOIN daftar_investors di ON s.daftar_id = di.daftar_id
            WHERE p.id = :pitch_id 
            AND di.investor_id = :investor_id
            AND di.is_active = true
        """),
        {
            "pitch_id": pitch_id,
            "investor_id": investor_id
        }
    )
    
    if not access_check.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pitch not found or investor does not have access"
        )
    
    # Create offer
    result = await db.execute(
        text("""
            INSERT INTO offers (
                pitch_id, investor_id, amount, equity_percentage,
                terms, status, valid_until, notes, created_at
            )
            VALUES (
                :pitch_id, :investor_id, :amount, :equity_percentage,
                :terms, 'pending', :valid_until, :notes, CURRENT_TIMESTAMP
            )
            RETURNING *
        """),
        {
            "pitch_id": pitch_id,
            "investor_id": investor_id,
            "amount": offer.amount,
            "equity_percentage": offer.equity_percentage,
            "terms": offer.terms,
            "valid_until": offer.valid_until,
            "notes": offer.notes
        }
    )
    
    await db.commit()
    return result.first()

@router.get("/pitches/{pitch_id}/offers", response_model=List[OfferResponse])
async def get_pitch_offers(
    pitch_id: int,
    investor_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all offers for a pitch"""
    # Get offers
    result = await db.execute(
        text("""
            SELECT * FROM offers
            WHERE pitch_id = :pitch_id
            AND investor_id = :investor_id
            ORDER BY created_at DESC
        """),
        {
            "pitch_id": pitch_id,
            "investor_id": investor_id
        }
    )
    
    offers = result.fetchall()
    return [dict(offer) for offer in offers]

@router.post("/offers/{offer_id}/action")
async def take_offer_action(
    offer_id: int,
    action: OfferActionCreate,
    investor_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Take action on an offer (withdraw)"""
    # Verify offer exists and belongs to investor
    offer_check = await db.execute(
        text("""
            SELECT status FROM offers
            WHERE id = :offer_id
            AND investor_id = :investor_id
        """),
        {
            "offer_id": offer_id,
            "investor_id": investor_id
        }
    )
    offer = offer_check.first()
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    if offer.status != 'pending':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot {action.action} offer with status {offer.status}"
        )
    
    if action.action != 'withdraw':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Investors can only withdraw offers"
        )
    
    # Update offer status
    await db.execute(
        text("""
            UPDATE offers
            SET status = 'withdrawn'
            WHERE id = :offer_id
        """),
        {"offer_id": offer_id}
    )
    
    # Record action
    await db.execute(
        text("""
            INSERT INTO offer_actions (
                offer_id, action, action_by, notes, action_taken_at
            )
            VALUES (
                :offer_id, :action, :investor_id, :notes, CURRENT_TIMESTAMP
            )
        """),
        {
            "offer_id": offer_id,
            "action": action.action,
            "investor_id": investor_id,
            "notes": action.notes
        }
    )
    
    await db.commit()
    return {"status": "success", "message": "Offer withdrawn successfully"}

@router.post("/pitches/{pitch_id}/bills", response_model=BillResponse)
async def create_bill(
    pitch_id: int,
    investor_id: int,
    bill: BillCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new bill for a pitch"""
    # Verify investor has access to create bills
    access_check = await db.execute(
        text("""
            SELECT 1 FROM pitches p
            JOIN scouts s ON p.scout_id = s.id
            JOIN daftar_investors di ON s.daftar_id = di.daftar_id
            WHERE p.id = :pitch_id 
            AND di.investor_id = :investor_id
            AND di.is_active = true
            AND di.role = 'admin'  # Only admins can create bills
        """),
        {
            "pitch_id": pitch_id,
            "investor_id": investor_id
        }
    )
    
    if not access_check.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create bills"
        )
    
    # Create bill
    result = await db.execute(
        text("""
            INSERT INTO bills (
                pitch_id, amount, description, due_date,
                payment_link, is_paid, created_at
            )
            VALUES (
                :pitch_id, :amount, :description, :due_date,
                :payment_link, false, CURRENT_TIMESTAMP
            )
            RETURNING *
        """),
        {
            "pitch_id": pitch_id,
            "amount": bill.amount,
            "description": bill.description,
            "due_date": bill.due_date,
            "payment_link": bill.payment_link
        }
    )
    
    await db.commit()
    return result.first() 