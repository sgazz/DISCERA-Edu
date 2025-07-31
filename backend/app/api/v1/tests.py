from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from ...core.database import get_db
from ...core.security import oauth2_scheme, verify_token
from ...models.user import User, UserRole
from ...models.test import Test, Question, TestResult, TestAnswer, DifficultyLevel, QuestionType

router = APIRouter()


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: QuestionType
    options: Optional[str]
    points: int

    class Config:
        from_attributes = True


class TestResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    difficulty: DifficultyLevel
    time_limit: Optional[int]
    is_active: bool
    created_at: datetime
    questions: List[QuestionResponse] = []

    class Config:
        from_attributes = True


class TestResultResponse(BaseModel):
    id: int
    score: int
    total_points: int
    percentage: int
    time_taken: Optional[int]
    completed_at: datetime

    class Config:
        from_attributes = True


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


@router.get("/", response_model=List[TestResponse])
async def get_tests(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tests based on user role."""
    if current_user.role == UserRole.ADMIN:
        # Admin can see all tests
        tests = db.query(Test).offset(skip).limit(limit).all()
    elif current_user.role == UserRole.TEACHER:
        # Teachers can see their own tests
        tests = db.query(Test).filter(Test.creator_id == current_user.id).offset(skip).limit(limit).all()
    else:
        # Students can see active tests
        tests = db.query(Test).filter(Test.is_active == True).offset(skip).limit(limit).all()
    
    return tests


@router.get("/{test_id}", response_model=TestResponse)
async def get_test(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific test."""
    test = db.query(Test).filter(Test.id == test_id).first()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.STUDENT and not test.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Test is not active"
        )
    
    if current_user.role == UserRole.TEACHER and test.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return test


@router.get("/{test_id}/results", response_model=List[TestResultResponse])
async def get_test_results(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get test results."""
    # Check if test exists
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    # Get results based on user role
    if current_user.role == UserRole.STUDENT:
        # Students can only see their own results
        results = db.query(TestResult).filter(
            TestResult.test_id == test_id,
            TestResult.student_id == current_user.id
        ).all()
    else:
        # Teachers and admins can see all results for their tests
        if current_user.role == UserRole.TEACHER and test.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        results = db.query(TestResult).filter(TestResult.test_id == test_id).all()
    
    return results


@router.post("/{test_id}/submit")
async def submit_test(
    test_id: int,
    answers: dict,  # {question_id: answer_text}
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit test answers and calculate results."""
    # Check if test exists and is active
    test = db.query(Test).filter(Test.id == test_id, Test.is_active == True).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found or not active"
        )
    
    # Get test questions
    questions = db.query(Question).filter(Question.test_id == test_id).all()
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Test has no questions"
        )
    
    # Calculate results
    total_points = sum(q.points for q in questions)
    score = 0
    test_answers = []
    
    for question in questions:
        answer_text = answers.get(str(question.id), "")
        is_correct = answer_text.lower().strip() == question.correct_answer.lower().strip()
        points_earned = question.points if is_correct else 0
        score += points_earned
        
        # Create test answer record
        test_answer = TestAnswer(
            question_id=question.id,
            answer_text=answer_text,
            is_correct=is_correct,
            points_earned=points_earned
        )
        test_answers.append(test_answer)
    
    # Calculate percentage
    percentage = int((score / total_points) * 100) if total_points > 0 else 0
    
    # Create test result
    test_result = TestResult(
        test_id=test_id,
        student_id=current_user.id,
        score=score,
        total_points=total_points,
        percentage=percentage
    )
    
    db.add(test_result)
    db.commit()
    db.refresh(test_result)
    
    # Add test answers
    for answer in test_answers:
        answer.test_result_id = test_result.id
        db.add(answer)
    
    db.commit()
    
    return {
        "test_result_id": test_result.id,
        "score": score,
        "total_points": total_points,
        "percentage": percentage
    } 