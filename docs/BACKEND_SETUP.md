# DISCERA Backend Setup

## 🏗️ **Trenutno stanje projekta**

### **✅ Završeno:**
1. **Osnovna struktura projekta**
   - FastAPI aplikacija ✅
   - SQLAlchemy database setup ✅
   - JWT autentifikacija ✅
   - Environment konfiguracija ✅
   - **Server radi na http://localhost:8001** ✅

2. **Database modeli**
   - `User` - Korisnički model sa rolama (admin, teacher, student) ✅
   - `Document` - Model za upload i upravljanje dokumentima ✅
   - `Conversation` - Model za AI chat konverzacije ✅
   - `Message` - Model za pojedinačne poruke u chat-u ✅

3. **Core funkcionalnosti**
   - Konfiguracija (`app/core/config.py`) ✅
   - Database setup (`app/core/database.py`) ✅
   - Security utilities (`app/core/security.py`) ✅
   - Pydantic schemas (`app/schemas/`) ✅

4. **API Endpoints**
   - Root endpoint (`/`) ✅
   - Health check (`/health`) ✅
   - Swagger UI (`/docs`) ✅

### **🔄 U toku:**
- RAG sistem implementacija
- AI servisi integracija
- Authentication endpoints

### **📋 Sledeći koraci:**
1. **RAG sistem** - Document processing pipeline
2. **AI servisi** - OpenAI i Ollama integracija
3. **Authentication** - Login/register endpoints
4. **File upload** - Document upload sistem
5. **Chat API** - AI conversation endpoints

## 🚀 **Pokretanje backend-a**

### **1. Instalacija zavisnosti**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **2. Environment setup**
```bash
cp env.example .env
# Uredite .env fajl sa vašim kredencijalima
```

### **3. Pokretanje aplikacije**
```bash
# Opcija 1: Direktno
python main.py

# Opcija 2: Uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8001

# Opcija 3: Python modul
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)"
```

### **4. API dokumentacija**
- **API Base URL:** http://localhost:8001
- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc
- **Health Check:** http://localhost:8001/health

## 📊 **Testiranje API-ja**

### **Root endpoint**
```bash
curl http://localhost:8001/
# Response: {"message":"DISCERA API","version":"1.0.0","status":"running"}
```

### **Health check**
```bash
curl http://localhost:8001/health
# Response: {"status":"healthy","database":"connected","timestamp":"2024-01-01T00:00:00Z"}
```

## 📊 **Database Schema**

### **Users tabela**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    role VARCHAR DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

### **Documents tabela**
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    file_path VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR NOT NULL,
    content TEXT,
    is_processed BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

### **Conversations tabela**
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    title VARCHAR,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

### **Messages tabela**
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    role VARCHAR NOT NULL,
    message_metadata JSON,
    conversation_id INTEGER REFERENCES conversations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 **Konfiguracija**

### **Development**
- SQLite database za lakše testiranje ✅
- Debug mode uključen ✅
- CORS omogućen za localhost ✅
- Virtual environment setup ✅

### **Production**
- PostgreSQL database
- Redis za caching
- Environment varijable za sve kredencijale

## 📝 **Test kredencijali**

```
Admin:     admin@discera.com / admin123
Teacher:   teacher@discera.com / teacher123
Student:   student@discera.com / student123
```

## 🎯 **Sledeći korak: RAG Sistem**

Sada kada imamo funkcionalan backend, sledeći korak je implementacija **RAG (Retrieval Augmented Generation)** sistema:

1. **Document Processing Pipeline**
2. **Embedding Generation**
3. **Vector Storage (ChromaDB)**
4. **Retrieval System**
5. **AI Integration**

---

**DISCERA Backend** - ✅ **FUNKCIONALAN** - Spreman za RAG implementaciju! 🚀 