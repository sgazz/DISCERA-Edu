from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum


class QuestionType(str, enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Test(Base):
    __tablename__ = "tests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    time_limit = Column(Integer, nullable=True)  # in minutes
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    creator = relationship("User", back_populates="tests")
    questions = relationship("Question", back_populates="test")
    results = relationship("TestResult", back_populates="test")
    
    def __repr__(self):
        return f"<Test(id={self.id}, title='{self.title}', creator_id={self.creator_id})>"


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    correct_answer = Column(Text, nullable=False)
    options = Column(Text, nullable=True)  # JSON string for multiple choice
    explanation = Column(Text, nullable=True)
    points = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign Keys
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    
    # Relationships
    test = relationship("Test", back_populates="questions")
    answers = relationship("TestAnswer", back_populates="question")
    
    def __repr__(self):
        return f"<Question(id={self.id}, test_id={self.test_id}, type='{self.question_type}')>"


class TestResult(Base):
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)
    time_taken = Column(Integer, nullable=True)  # in seconds
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign Keys
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    test = relationship("Test", back_populates="results")
    student = relationship("User", back_populates="test_results")
    answers = relationship("TestAnswer", back_populates="test_result")
    
    def __repr__(self):
        return f"<TestResult(id={self.id}, test_id={self.test_id}, student_id={self.student_id}, score={self.score})>"


class TestAnswer(Base):
    __tablename__ = "test_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    points_earned = Column(Integer, default=0)
    
    # Foreign Keys
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    test_result_id = Column(Integer, ForeignKey("test_results.id"), nullable=False)
    
    # Relationships
    question = relationship("Question", back_populates="answers")
    test_result = relationship("TestResult", back_populates="answers")
    
    def __repr__(self):
        return f"<TestAnswer(id={self.id}, question_id={self.question_id}, is_correct={self.is_correct})>" 