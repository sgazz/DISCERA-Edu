#!/usr/bin/env python3
"""
Test database models
"""
from app.core.database import engine, Base
from app.models import user, document, conversation
from sqlalchemy import text

def test_models():
    """Test database models"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Test table creation
        with engine.connect() as conn:
            # Check if tables exist
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            print(f"✅ Tables found: {tables}")
            
            # Check specific tables
            expected_tables = ['users', 'documents', 'conversations', 'messages']
            for table in expected_tables:
                if table in tables:
                    print(f"✅ Table '{table}' exists")
                else:
                    print(f"❌ Table '{table}' missing")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

if __name__ == "__main__":
    test_models() 