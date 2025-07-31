"""
Document API endpoints for DISCERA
"""
import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.document import Document
from app.rag.rag_service import RAGService
from app.schemas.user import User as UserSchema

router = APIRouter(prefix="/documents", tags=["documents"])

# Initialize RAG service
rag_service = RAGService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: str = None,
    description: str = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    try:
        
        # Validate file type
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Validate file size
        if file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE} bytes"
            )
        
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create document record
        document = Document(
            title=title or file.filename,
            description=description,
            file_path=file_path,
            file_name=file.filename,
            file_size=file.size,
            file_type=file_extension,
            user_id=user.id
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Process document with RAG
        try:
            rag_result = rag_service.process_and_store_document(
                file_path=file_path,
                file_type=file_extension,
                document_id=str(document.id),
                metadata={
                    "user_id": user.id,
                    "title": document.title,
                    "file_type": file_extension
                }
            )
            
            # Update document with processing results
            document.content = rag_result.get("total_content_length", 0)
            document.is_processed = True
            db.commit()
            
            return {
                "success": True,
                "document_id": document.id,
                "title": document.title,
                "file_name": document.file_name,
                "file_size": document.file_size,
                "rag_processing": rag_result
            }
            
        except Exception as e:
            # If RAG processing fails, still save document but mark as not processed
            document.is_processed = False
            db.commit()
            
            return {
                "success": True,
                "document_id": document.id,
                "title": document.title,
                "file_name": document.file_name,
                "file_size": document.file_size,
                "warning": f"Document saved but RAG processing failed: {str(e)}"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@router.get("/", response_model=List[dict])
async def get_user_documents(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents for current user"""
    try:
        
        documents = db.query(Document).filter(Document.user_id == user.id).all()
        
        return [
            {
                "id": doc.id,
                "title": doc.title,
                "description": doc.description,
                "file_name": doc.file_name,
                "file_size": doc.file_size,
                "file_type": doc.file_type,
                "is_processed": doc.is_processed,
                "created_at": doc.created_at,
                "updated_at": doc.updated_at
            }
            for doc in documents
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get documents: {str(e)}"
        )


@router.get("/{document_id}")
async def get_document(
    document_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific document details"""
    try:
        
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == user.id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "id": document.id,
            "title": document.title,
            "description": document.description,
            "file_name": document.file_name,
            "file_size": document.file_size,
            "file_type": document.file_type,
            "is_processed": document.is_processed,
            "created_at": document.created_at,
            "updated_at": document.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get document: {str(e)}"
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document"""
    try:
        
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == user.id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete file from disk
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from RAG system
        try:
            rag_service.delete_document(str(document.id))
        except Exception as e:
            # Log error but continue with database deletion
            print(f"Warning: Failed to delete from RAG: {e}")
        
        # Delete from database
        db.delete(document)
        db.commit()
        
        return {"success": True, "message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        ) 