#!/usr/bin/env python3
"""
Test configuration
"""
from app.core.config import settings

def test_config():
    """Test configuration settings"""
    try:
        print("🔧 Testing DISCERA Configuration:")
        print(f"   App Name: {settings.APP_NAME}")
        print(f"   App Version: {settings.APP_VERSION}")
        print(f"   Debug Mode: {settings.DEBUG}")
        print(f"   Host: {settings.HOST}")
        print(f"   Port: {settings.PORT}")
        print(f"   Database URL: {settings.DATABASE_URL}")
        print(f"   Redis URL: {settings.REDIS_URL}")
        print(f"   JWT Algorithm: {settings.JWT_ALGORITHM}")
        print(f"   Token Expire Minutes: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
        print(f"   Upload Directory: {settings.UPLOAD_DIR}")
        print(f"   Max File Size: {settings.MAX_FILE_SIZE} bytes")
        print(f"   Allowed Extensions: {settings.ALLOWED_EXTENSIONS}")
        print(f"   ChromaDB Directory: {settings.CHROMA_PERSIST_DIRECTORY}")
        print("✅ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    test_config() 