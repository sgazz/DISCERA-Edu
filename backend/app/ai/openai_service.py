"""
OpenAI Service for DISCERA AI Integration
"""
import logging
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """OpenAI service for DISCERA AI features"""
    
    def __init__(self):
        """Initialize OpenAI service"""
        self.client = None
        self.model = "gpt-4"
        
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("✅ OpenAI service initialized")
        else:
            logger.warning("⚠️ OpenAI API key not configured")
    
    def generate_response(
        self, 
        query: str, 
        context: str = "",
        system_prompt: str = "",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate AI response using OpenAI"""
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "OpenAI client not initialized"
                }
            
            # Build messages
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            if context:
                # Add context as system message
                context_message = f"""You are a helpful AI assistant for DISCERA. Use the following context to answer the user's question:

Context:
{context}

Please provide a comprehensive and accurate answer based on the context provided."""
                messages.append({"role": "system", "content": context_message})
            
            # Add user query
            messages.append({"role": "user", "content": query})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "model": self.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_test_questions(
        self, 
        content: str, 
        num_questions: int = 5,
        question_types: List[str] = ["multiple_choice", "true_false", "short_answer"]
    ) -> Dict[str, Any]:
        """Generate test questions from content"""
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "OpenAI client not initialized"
                }
            
            system_prompt = f"""You are an expert educator creating test questions. Generate {num_questions} diverse test questions from the provided content.

Question types to include: {', '.join(question_types)}

For each question, provide:
1. Question text
2. Question type (multiple_choice, true_false, short_answer)
3. Correct answer
4. Options (for multiple choice)
5. Difficulty level (easy, medium, hard)

Format the response as JSON:
{{
    "questions": [
        {{
            "question": "Question text",
            "type": "multiple_choice",
            "correct_answer": "Correct answer",
            "options": ["A", "B", "C", "D"],
            "difficulty": "medium"
        }}
    ]
}}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate test questions from this content:\n\n{content}"}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating test questions: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_document(self, content: str) -> Dict[str, Any]:
        """Analyze document and extract key information"""
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "OpenAI client not initialized"
                }
            
            system_prompt = """Analyze the provided document and extract key information. Provide:

1. Main topics and themes
2. Key concepts and definitions
3. Important facts and figures
4. Difficulty level assessment
5. Suggested learning objectives
6. Potential test topics

Format as structured analysis."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this document:\n\n{content}"}
                ],
                max_tokens=1500,
                temperature=0.5
            )
            
            return {
                "success": True,
                "analysis": response.choices[0].message.content,
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing document: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        return self.client is not None and settings.OPENAI_API_KEY is not None 