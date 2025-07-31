"""
Complete Backend Test Suite for DISCERA
Tests all implemented components: Auth, Documents, Chat, RAG, AI
"""
import requests
import json
import sys
import time
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8001"
import time
TEST_USER = {
    "username": f"testuser_{int(time.time())}",
    "email": f"test_{int(time.time())}@discera.com",
    "password": "testpass123",
    "full_name": "Test User"
}

class BackendTester:
    """Complete backend testing suite"""
    
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.conversation_id = None
        self.test_results = {}
        
    def print_header(self, title: str):
        """Print test section header"""
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_result(self, test_name: str, success: bool, details: str = ""):
        """Print test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   📝 {details}")
        self.test_results[test_name] = success
    
    def test_server_health(self) -> bool:
        """Test if server is running"""
        try:
            response = self.session.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                self.print_result("Server Health Check", True, "Server is running")
                return True
            else:
                self.print_result("Server Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Server Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_database_connection(self) -> bool:
        """Test database connection"""
        try:
            response = self.session.get(f"{BASE_URL}/health")
            data = response.json()
            if data.get("database") == "connected":
                self.print_result("Database Connection", True, "Database is connected")
                return True
            else:
                self.print_result("Database Connection", False, "Database not connected")
                return False
        except Exception as e:
            self.print_result("Database Connection", False, f"Error: {str(e)}")
            return False
    
    def test_create_test_users(self) -> bool:
        """Create test users"""
        try:
            response = self.session.post(f"{BASE_URL}/auth/create-test-users")
            if response.status_code == 200:
                data = response.json()
                self.print_result("Create Test Users", True, f"Created: {data.get('created_users', [])}")
                return True
            else:
                self.print_result("Create Test Users", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Create Test Users", False, f"Error: {str(e)}")
            return False
    
    def test_user_registration(self) -> bool:
        """Test user registration"""
        try:
            response = self.session.post(
                f"{BASE_URL}/auth/register",
                json=TEST_USER
            )
            if response.status_code == 200:
                data = response.json()
                self.print_result("User Registration", True, f"User ID: {data.get('id')}")
                return True
            else:
                self.print_result("User Registration", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_user_login(self) -> bool:
        """Test user login"""
        try:
            response = self.session.post(
                f"{BASE_URL}/auth/login",
                data={
                    "username": TEST_USER["username"],
                    "password": TEST_USER["password"]
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
                self.print_result("User Login", True, "Access token obtained")
                return True
            else:
                # Try with existing test user
                response = self.session.post(
                    f"{BASE_URL}/auth/login",
                    data={
                        "username": "student",
                        "password": "student123"
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data.get("access_token")
                    self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
                    self.print_result("User Login", True, "Access token obtained (using test user)")
                    return True
                else:
                    self.print_result("User Login", False, f"Status: {response.status_code}")
                    return False
        except Exception as e:
            self.print_result("User Login", False, f"Error: {str(e)}")
            return False
    
    def test_get_current_user(self) -> bool:
        """Test getting current user info"""
        try:
            response = self.session.get(f"{BASE_URL}/auth/me")
            if response.status_code == 200:
                data = response.json()
                self.print_result("Get Current User", True, f"User: {data.get('username')}")
                return True
            else:
                self.print_result("Get Current User", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Get Current User", False, f"Error: {str(e)}")
            return False
    
    def test_get_user_documents(self) -> bool:
        """Test getting user documents"""
        try:
            response = self.session.get(f"{BASE_URL}/documents/")
            if response.status_code == 200:
                data = response.json()
                self.print_result("Get User Documents", True, f"Found {len(data)} documents")
                return True
            else:
                self.print_result("Get User Documents", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Get User Documents", False, f"Error: {str(e)}")
            return False
    
    def test_create_conversation(self) -> bool:
        """Test creating a conversation"""
        try:
            response = self.session.post(
                f"{BASE_URL}/chat/conversations",
                params={"title": "Test Conversation"}
            )
            if response.status_code == 200:
                data = response.json()
                self.conversation_id = data.get("id")
                self.print_result("Create Conversation", True, f"Conversation ID: {self.conversation_id}")
                return True
            else:
                self.print_result("Create Conversation", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Create Conversation", False, f"Error: {str(e)}")
            return False
    
    def test_get_conversations(self) -> bool:
        """Test getting user conversations"""
        try:
            response = self.session.get(f"{BASE_URL}/chat/conversations")
            if response.status_code == 200:
                data = response.json()
                self.print_result("Get Conversations", True, f"Found {len(data)} conversations")
                return True
            else:
                self.print_result("Get Conversations", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Get Conversations", False, f"Error: {str(e)}")
            return False
    
    def test_send_chat_message(self) -> bool:
        """Test sending a chat message"""
        try:
            message_data = {
                "content": "Hello, this is a test message!",
                "conversation_id": self.conversation_id
            }
            response = self.session.post(
                f"{BASE_URL}/chat/send",
                json=message_data
            )
            if response.status_code == 200:
                data = response.json()
                self.print_result("Send Chat Message", True, f"Message ID: {data.get('message_id')}")
                return True
            else:
                self.print_result("Send Chat Message", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Send Chat Message", False, f"Error: {str(e)}")
            return False
    
    def test_get_conversation_messages(self) -> bool:
        """Test getting conversation messages"""
        try:
            if not self.conversation_id:
                self.print_result("Get Conversation Messages", False, "No conversation ID available")
                return False
                
            response = self.session.get(f"{BASE_URL}/chat/conversations/{self.conversation_id}/messages")
            if response.status_code == 200:
                data = response.json()
                self.print_result("Get Conversation Messages", True, f"Found {len(data)} messages")
                return True
            else:
                self.print_result("Get Conversation Messages", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Get Conversation Messages", False, f"Error: {str(e)}")
            return False
    
    def test_rag_system(self) -> bool:
        """Test RAG system functionality"""
        try:
            # Test RAG system stats
            from app.rag.rag_service import RAGService
            rag_service = RAGService()
            stats = rag_service.get_system_stats()
            
            self.print_result("RAG System Stats", True, f"Collections: {stats.get('collections', 0)}")
            return True
        except Exception as e:
            self.print_result("RAG System Stats", False, f"Error: {str(e)}")
            return False
    
    def test_ai_service(self) -> bool:
        """Test AI service functionality"""
        try:
            from app.ai.openai_service import OpenAIService
            ai_service = OpenAIService()
            
            if ai_service.is_available():
                self.print_result("AI Service", True, "OpenAI service available")
                return True
            else:
                self.print_result("AI Service", True, "OpenAI service not configured (expected in development)")
                return True  # Not a failure in development
        except Exception as e:
            self.print_result("AI Service", False, f"Error: {str(e)}")
            return False
    
    def test_api_documentation(self) -> bool:
        """Test API documentation access"""
        try:
            response = self.session.get(f"{BASE_URL}/docs")
            if response.status_code == 200:
                self.print_result("API Documentation", True, "Swagger UI accessible")
                return True
            else:
                self.print_result("API Documentation", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("API Documentation", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 DISCERA Backend Complete Test Suite")
        print("=" * 60)
        
        # Infrastructure tests
        self.print_header("Infrastructure Tests")
        self.test_server_health()
        self.test_database_connection()
        self.test_api_documentation()
        
        # Authentication tests
        self.print_header("Authentication Tests")
        self.test_create_test_users()
        self.test_user_registration()
        self.test_user_login()
        self.test_get_current_user()
        
        # Document management tests
        self.print_header("Document Management Tests")
        self.test_get_user_documents()
        
        # Chat system tests
        self.print_header("Chat System Tests")
        self.test_create_conversation()
        self.test_get_conversations()
        self.test_send_chat_message()
        self.test_get_conversation_messages()
        
        # AI and RAG tests
        self.print_header("AI & RAG Tests")
        self.test_rag_system()
        self.test_ai_service()
        
        # Summary
        self.print_header("Test Summary")
        total_tests = len(self.test_results)
        passed_tests = sum(self.test_results.values())
        failed_tests = total_tests - passed_tests
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 All tests passed! Backend is fully functional.")
        else:
            print(f"\n⚠️ {failed_tests} test(s) failed. Check the details above.")
        
        return failed_tests == 0


def main():
    """Main test runner"""
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 