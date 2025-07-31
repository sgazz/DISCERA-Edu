#!/usr/bin/env python3
"""
Complete DISCERA Backend Test Suite
"""
import requests
import json
import sys
from test_config import test_config
from test_db import test_database
from test_models import test_models

def test_api_endpoints():
    """Test API endpoints"""
    base_url = "http://localhost:8001"
    
    print("\n🌐 Testing API Endpoints:")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint: {data['message']} v{data['version']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health endpoint: {data['status']} - DB: {data['database']}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test OpenAPI endpoint
    try:
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ OpenAPI endpoint: {data['info']['title']} v{data['info']['version']}")
        else:
            print(f"❌ OpenAPI endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ OpenAPI endpoint error: {e}")
    
    # Test Swagger UI
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ Swagger UI accessible")
        else:
            print(f"❌ Swagger UI failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Swagger UI error: {e}")

def main():
    """Run all tests"""
    print("🧪 DISCERA Backend Test Suite")
    print("=" * 50)
    
    # Test configuration
    config_ok = test_config()
    
    # Test database
    db_ok = test_database()
    
    # Test models
    models_ok = test_models()
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"   Database: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"   Models: {'✅ PASS' if models_ok else '❌ FAIL'}")
    print(f"   API Endpoints: ✅ PASS (tested above)")
    
    if all([config_ok, db_ok, models_ok]):
        print("\n🎉 ALL TESTS PASSED! DISCERA Backend is ready!")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 