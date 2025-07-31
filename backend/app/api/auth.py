"""
Authentication API endpoints for DISCERA
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_current_user_from_token, get_current_user
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, User as UserSchema, Token
from app.core.security import get_password_hash

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", response_model=UserSchema)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return access token"""
    try:
        # Find user by username or email
        user = db.query(User).filter(
            (User.username == form_data.username) | (User.email == form_data.username)
        ).first()
        
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=UserSchema)
async def get_current_user(user: User = Depends(get_current_user)):
    """Get current user information"""
    return user


@router.post("/create-test-users")
async def create_test_users(db: Session = Depends(get_db)):
    """Create test users for development"""
    try:
        test_users = [
            {
                "email": "admin@discera.com",
                "username": "admin",
                "password": "admin123",
                "full_name": "Admin User",
                "role": UserRole.ADMIN
            },
            {
                "email": "teacher@discera.com", 
                "username": "teacher",
                "password": "teacher123",
                "full_name": "Teacher User",
                "role": UserRole.TEACHER
            },
            {
                "email": "student@discera.com",
                "username": "student", 
                "password": "student123",
                "full_name": "Student User",
                "role": UserRole.STUDENT
            }
        ]
        
        created_users = []
        for user_data in test_users:
            # Check if user exists
            existing_user = db.query(User).filter(
                (User.email == user_data["email"]) | (User.username == user_data["username"])
            ).first()
            
            if not existing_user:
                hashed_password = get_password_hash(user_data["password"])
                new_user = User(
                    email=user_data["email"],
                    username=user_data["username"],
                    hashed_password=hashed_password,
                    full_name=user_data["full_name"],
                    role=user_data["role"],
                    is_verified=True
                )
                db.add(new_user)
                created_users.append(user_data["username"])
        
        db.commit()
        
        return {
            "message": "Test users created successfully",
            "created_users": created_users
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create test users: {str(e)}"
        ) 