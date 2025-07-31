"""
Chat API endpoints for DISCERA AI conversations
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.rag.rag_service import RAGService
from app.ai.openai_service import OpenAIService

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize services
rag_service = RAGService()
ai_service = OpenAIService()


class ChatMessage(BaseModel):
    """Chat message request model"""
    content: str
    conversation_id: int = None


class ChatResponse(BaseModel):
    """Chat response model"""
    message_id: int
    content: str
    role: str
    conversation_id: int
    metadata: Optional[Dict[str, Any]] = None


@router.post("/conversations", response_model=Dict[str, Any])
async def create_conversation(
    title: str = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    try:
        
        conversation = Conversation(
            title=title or "New Conversation",
            user_id=user.id
        )
        
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create conversation: {str(e)}"
        )


@router.get("/conversations", response_model=List[Dict[str, Any]])
async def get_conversations(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for current user"""
    try:
        
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user.id
        ).all()
        
        return [
            {
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at
            }
            for conv in conversations
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get conversations: {str(e)}"
        )


@router.get("/conversations/{conversation_id}/messages", response_model=List[ChatResponse])
async def get_conversation_messages(
    conversation_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation"""
    try:
        
        # Verify conversation belongs to user
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        return [
            ChatResponse(
                message_id=msg.id,
                content=msg.content,
                role=msg.role,
                conversation_id=msg.conversation_id,
                metadata=msg.message_metadata
            )
            for msg in messages
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get messages: {str(e)}"
        )


@router.post("/send", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message and get AI response"""
    try:
        
        # Get or create conversation
        if message.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == message.conversation_id,
                Conversation.user_id == user.id
            ).first()
            
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(
                title="New Conversation",
                user_id=user.id
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Save user message
        user_message = Message(
            content=message.content,
            role="user",
            conversation_id=conversation.id
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Get context from RAG
        context = rag_service.get_context_for_query(message.content, n_results=3)
        
        # Generate AI response
        ai_response = ai_service.generate_response(
            query=message.content,
            context=context,
            system_prompt="You are a helpful AI assistant for DISCERA. Provide accurate and helpful responses based on the context provided."
        )
        
        if ai_response["success"]:
            # Save AI response
            ai_message = Message(
                content=ai_response["response"],
                role="assistant",
                conversation_id=conversation.id,
                message_metadata={
                    "model": ai_response.get("model", "unknown"),
                    "usage": ai_response.get("usage", {}),
                    "context_length": len(context)
                }
            )
            db.add(ai_message)
            db.commit()
            db.refresh(ai_message)
            
            return ChatResponse(
                message_id=ai_message.id,
                content=ai_message.content,
                role=ai_message.role,
                conversation_id=ai_message.conversation_id,
                metadata=ai_message.message_metadata
            )
        else:
            # If AI fails, return error message
            error_message = Message(
                content="Sorry, I'm having trouble processing your request. Please try again.",
                role="assistant",
                conversation_id=conversation.id,
                message_metadata={"error": ai_response.get("error", "Unknown error")}
            )
            db.add(error_message)
            db.commit()
            db.refresh(error_message)
            
            return ChatResponse(
                message_id=error_message.id,
                content=error_message.content,
                role=error_message.role,
                conversation_id=error_message.conversation_id,
                metadata=error_message.message_metadata
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send message: {str(e)}"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a conversation and all its messages"""
    try:
        
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Delete all messages in conversation
        db.query(Message).filter(Message.conversation_id == conversation_id).delete()
        
        # Delete conversation
        db.delete(conversation)
        db.commit()
        
        return {"success": True, "message": "Conversation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete conversation: {str(e)}"
        ) 