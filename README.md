# DISCERA - Digital Intelligent System for Comprehensive Exam Review & Assessment

## 🎯 **Šta je DISCERA?**

DISCERA je napredan digitalni sistem za inteligentnu analizu dokumenata, generisanje testova i AI-asistirano učenje. Sistem je dizajniran da transformiše način na koji studenti i nastavnici pristupaju edukaciji.

## 🚀 **Glavne funkcionalnosti**

### 📚 **Document Management**
- **Upload dokumenata** - Podržava PDF, DOC, DOCX, TXT fajlove
- **Inteligentna obrada** - Automatska ekstrakcija teksta i strukture
- **Organizacija** - Kategorizacija i tagovanje materijala
- **Pretraga** - Napredna pretraga kroz sve dokumente

### 🤖 **AI Assistant**
- **Chat sa AI** - Postavljajte pitanja o vašim dokumentima
- **Kontekstualni odgovori** - AI razume sadržaj vaših materijala
- **Inteligentna analiza** - Automatsko prepoznavanje ključnih koncepata
- **Personalizovani pristup** - Prilagođava se vašem stilu učenja

### 📝 **Test Generation**
- **Automatsko generisanje** - AI kreira testove iz vaših materijala
- **Različiti tipovi pitanja** - Multiple choice, true/false, kratki odgovori
- **Nivoi težine** - Easy, medium, hard pitanja
- **Personalizovani testovi** - Prilagođeni vašim potrebama

### 📊 **Analytics & Progress Tracking**
- **Detaljna analitika** - Praćenje napretka i performansi
- **Success rate** - Procenat uspešnosti na testovima
- **Learning insights** - Prepoznavanje slabih oblasti
- **Progress reports** - Detaljni izveštaji o napretku

## 🛠️ **Tehnologije**

### **Backend**
- **FastAPI** - Brz i moderan Python web framework
- **SQLAlchemy** - ORM za bazu podataka
- **SQLite** - Baza podataka (development)
- **PostgreSQL** - Baza podataka (production)
- **JWT** - Autentifikacija i autorizacija

### **AI/ML Stack**
- **OpenAI API** - GPT-4 za chat i test generation
- **Ollama** - Lokalni LLM (Mistral, Llama2)
- **ChromaDB** - Vector database
- **Sentence Transformers** - Embeddings
- **LangChain** - RAG implementation

## 🚀 **Pokretanje projekta**

### **1. Kloniranje i setup**
```bash
git clone <repository-url>
cd DISCERA
```

### **2. Virtualno okruženje**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ili
venv\Scripts\activate  # Windows
```

### **3. Instalacija zavisnosti**
```bash
pip install -r requirements.txt
```

### **4. Pokretanje DISCERA Assistant skripte**
```bash
./DISCERA_Assistant.command
```

### **5. Manualno pokretanje**
```bash
# Backend
cd backend
python main.py

# Frontend (kada bude implementiran)
cd frontend
npm install
npm run dev
```

## 🌐 **Pristup aplikaciji**

- **Backend API**: http://localhost:8001
- **API Dokumentacija**: http://localhost:8001/docs
- **Frontend**: http://localhost:3000 (kada bude implementiran)

## 👥 **Korisničke role**

### **Admin**
- Pristup svim funkcionalnostima
- Upravljanje korisnicima
- Sistem administracija

### **Teacher**
- Kreiranje i upravljanje testovima
- Upload i organizacija materijala
- Praćenje napretka studenata

### **Student**
- Pristup materijalima
- Polaganje testova
- Praćenje sopstvenog napretka

## 🧪 **Test kredencijali**

```
Admin:     admin@discera.com / admin123
Teacher:   teacher@discera.com / teacher123
Student:   student@discera.com / student123
```

## 📁 **Struktura projekta**

```
DESCERA/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── documents.py
│   │   │   ├── tests.py
│   │   │   └── ai.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   └── test.py
│   │   └── services/
│   ├── main.py
│   └── requirements.txt
├── frontend/ (u razvoju)
├── uploads/
├── chroma_db/
├── DISCERA_Assistant.command
└── README.md
```

## 🔧 **Konfiguracija**

Kreirajte `.env` fajl u root direktorijumu:

```env
# App
APP_NAME=DISCERA
APP_VERSION=1.0.0
DEBUG=true

# Database
DATABASE_URL=sqlite:///./discera.db

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI/ML
OPENAI_API_KEY=your-openai-api-key-here
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_DB_PATH=./chroma_db

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=[".pdf", ".doc", ".docx", ".txt"]
```

## 🧪 **Testiranje**

```bash
# Pokretanje testova
cd backend
pytest

# Pokretanje sa coverage
pytest --cov=app
```

## 📝 **API Endpoints**

### **Authentication**
- `POST /api/v1/auth/register` - Registracija korisnika
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Trenutni korisnik

### **Users**
- `GET /api/v1/users/` - Lista korisnika (admin)
- `GET /api/v1/users/{user_id}` - Detalji korisnika

### **Documents**
- `POST /api/v1/documents/upload` - Upload dokumenta
- `GET /api/v1/documents/` - Lista dokumenata
- `GET /api/v1/documents/{document_id}` - Detalji dokumenta
- `DELETE /api/v1/documents/{document_id}` - Brisanje dokumenta

### **Tests**
- `GET /api/v1/tests/` - Lista testova
- `GET /api/v1/tests/{test_id}` - Detalji testa
- `POST /api/v1/tests/{test_id}/submit` - Predaja testa

### **AI**
- `POST /api/v1/ai/chat` - Chat sa AI
- `POST /api/v1/ai/generate-test` - Generisanje testa
- `GET /api/v1/ai/documents/{document_id}/analyze` - Analiza dokumenta

## 🌟 **Ključne prednosti**

### **Za studente:**
- **Personalizovano učenje** - AI prilagođava sadržaj vašim potrebama
- **Efikasna priprema** - Fokus na oblasti koje trebate da poboljšate
- **Interaktivno iskustvo** - Chat sa AI o vašim materijalima
- **Praćenje napretka** - Jasna vizija vašeg napretka

### **Za nastavnike:**
- **Automatizacija** - AI generiše testove umesto vas
- **Vremenska efikasnost** - Manje vremena na administrativne zadatke
- **Kvalitetan sadržaj** - AI kreira raznovrsne i relevantne testove
- **Analitika** - Detaljni uvid u napredak studenata

### **Za institucije:**
- **Skalabilnost** - Podržava veliki broj korisnika
- **Kost efektivnost** - Smanjuje troškove testiranja
- **Kvalitet** - Konzistentan kvalitet edukacije
- **Inovacija** - Moderni pristup edukaciji

## 🔮 **Budući razvoj**

- **Mobile app** - iOS i Android aplikacije
- **Advanced AI** - Više AI modela i tehnika
- **Collaborative features** - Grupno učenje i saradnja
- **Integration** - Integracija sa LMS sistemima
- **Analytics dashboard** - Napredna analitika i izveštaji

## 📄 **Licenca**

MIT License

## 🤝 **Doprinosi**

Dobrodošli su svi doprinosi! Molimo vas da:

1. Fork-ujte projekat
2. Kreirajte feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit-ujte promene (`git commit -m 'Add some AmazingFeature'`)
4. Push-ujte na branch (`git push origin feature/AmazingFeature`)
5. Otvorite Pull Request

## 📞 **Kontakt**

- **Email**: support@discera.com
- **Website**: https://discera.com
- **GitHub**: https://github.com/discera

---

**DISCERA** - Transformišemo način na koji se uči i testira! 🚀 