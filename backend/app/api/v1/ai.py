from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import json

from ...core.database import get_db
from ...core.security import oauth2_scheme, verify_token
from ...core.config import settings
from ...models.user import User, UserRole
from ...models.document import Document

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    document_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []


class TestGenerationRequest(BaseModel):
    document_id: int
    num_questions: int = 10
    difficulty: str = "medium"
    question_types: List[str] = ["multiple_choice", "true_false"]


class TestGenerationResponse(BaseModel):
    test_id: int
    title: str
    questions: List[dict]


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user from token."""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    chat_request: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI about documents."""
    # For now, return a simple response
    # In the future, this will integrate with OpenAI or Ollama
    
    if chat_request.document_id:
        # Get document content
        document = db.query(Document).filter(
            Document.id == chat_request.document_id,
            Document.owner_id == current_user.id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        response = f"AI Assistant: I can help you with questions about '{document.title}'. What would you like to know?"
    else:
        response = "AI Assistant: Hello! I'm here to help you with your documents and learning. You can ask me questions about your uploaded materials or request help with test preparation."
    
    return ChatResponse(
        response=response,
        sources=[]
    )


@router.post("/generate-test", response_model=TestGenerationResponse)
async def generate_test(
    request: TestGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a test from document content."""
    # Check if user can create tests
    if current_user.role not in [UserRole.TEACHER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers and admins can generate tests"
        )
    
    # Get document
    document = db.query(Document).filter(
        Document.id == request.document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if not document.is_processed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document is not processed yet. Please wait for processing to complete."
        )
    
    # For now, return a mock test
    # In the future, this will use AI to generate actual questions
    
    mock_questions = [
        {
            "question_text": "What is the main topic of this document?",
            "question_type": "multiple_choice",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A",
            "points": 1
        },
        {
            "question_text": "True or False: This document contains important information.",
            "question_type": "true_false",
            "correct_answer": "True",
            "points": 1
        }
    ]
    
    return TestGenerationResponse(
        test_id=1,
        title=f"Test generated from {document.title}",
        questions=mock_questions
    )


@router.get("/documents/{document_id}/analyze")
async def analyze_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze document content and extract key concepts."""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Mock analysis - in the future, this will use AI
    analysis = {
        "key_concepts": ["concept1", "concept2", "concept3"],
        "summary": "This is a mock summary of the document content.",
        "difficulty_level": "medium",
        "estimated_reading_time": "5 minutes",
        "topics": ["topic1", "topic2"]
    }
    
    return analysis 