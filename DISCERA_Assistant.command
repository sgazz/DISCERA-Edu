#!/bin/bash

# DISCERA Assistant - Complete Development Environment
# Digital Intelligent System for Comprehensive Exam Review & Assessment

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🚀 Starting DISCERA - Digital Intelligent System for Comprehensive Exam Review & Assessment${NC}"
echo "=================================================================================="

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Function to kill processes on a port
kill_port() {
    local port=$1
    if check_port $port; then
        echo -e "${YELLOW}⚠️  Port $port is already in use. Stopping existing process...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null
        sleep 2
    fi
}

# Function to start backend
start_backend() {
    echo -e "${CYAN}🔧 Activating virtual environment...${NC}"
    source venv/bin/activate
    
    echo -e "${CYAN}📥 Installing Python dependencies...${NC}"
    pip install -r requirements.txt > /dev/null 2>&1
    
    echo -e "${CYAN}📁 Creating necessary directories...${NC}"
    mkdir -p uploads
    mkdir -p chroma_db
    
    echo -e "${CYAN}🔍 Checking port availability...${NC}"
    kill_port 8001
    
    echo -e "${CYAN}🔧 Starting DISCERA Backend Server (FastAPI) on port 8001...${NC}"
    echo -e "${GREEN}📚 API Documentation will be available at: http://localhost:8001/docs${NC}"
    echo -e "${GREEN}🔍 Health check: http://localhost:8001/health${NC}"
    
    # Start backend in background
    cd backend
    uvicorn main:app --host 0.0.0.0 --port 8001 --reload > ../backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    echo -e "${YELLOW}⏳ Waiting for backend to start...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:8001/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Backend server is running!${NC}"
            break
        fi
        sleep 1
    done
}

# Function to start frontend
start_frontend() {
    echo -e "${CYAN}🔍 Checking frontend port availability...${NC}"
    kill_port 3000
    kill_port 3001
    
    echo -e "${CYAN}🔧 Starting DISCERA Frontend Server (Next.js) on port 3000...${NC}"
    echo -e "${GREEN}🌐 Frontend will be available at: http://localhost:3000${NC}"
    
    # Check if we're in the frontend directory
    if [ ! -f "frontend/package.json" ]; then
        echo -e "${RED}❌ Error: package.json not found in frontend directory${NC}"
        exit 1
    fi
    
    # Install frontend dependencies if needed
    if [ ! -d "frontend/node_modules" ]; then
        echo -e "${CYAN}📦 Installing frontend dependencies...${NC}"
        cd frontend
        npm install > /dev/null 2>&1
        cd ..
    fi
    
    # Start frontend in background
    cd frontend
    npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    # Wait for frontend to start
    echo -e "${YELLOW}⏳ Waiting for frontend to start...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Frontend server is running!${NC}"
            break
        fi
        sleep 1
    done
}

# Function to open browser
open_browser() {
    echo -e "${CYAN}🌐 Opening browser...${NC}"
    sleep 3
    open http://localhost:3000
    open http://localhost:8001/docs
}

# Function to show status
show_status() {
    echo -e "${PURPLE}📊 Current Status:${NC}"
    echo -e "${CYAN}Backend:${NC} $(check_port 8001 && echo -e "${GREEN}✅ Running${NC}" || echo -e "${RED}❌ Stopped${NC}")"
    echo -e "${CYAN}Frontend:${NC} $(check_port 3000 && echo -e "${GREEN}✅ Running${NC}" || echo -e "${RED}❌ Stopped${NC}")"
    echo ""
    echo -e "${GREEN}🎉 DISCERA is ready!${NC}"
    echo -e "${BLUE}Frontend:${NC} http://localhost:3000"
    echo -e "${BLUE}Backend API:${NC} http://localhost:8001"
    echo -e "${BLUE}API Documentation:${NC} http://localhost:8001/docs"
    echo -e "${BLUE}Health Check:${NC} http://localhost:8001/health"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
}

# Function to cleanup on exit
cleanup() {
    echo -e "${YELLOW}🛑 Stopping DISCERA servers...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    kill_port 8001
    kill_port 3000
    kill_port 3001
    echo -e "${GREEN}✅ Servers stopped${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
echo -e "${CYAN}🔍 Checking environment...${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Error: Virtual environment not found. Please run setup first.${NC}"
    exit 1
fi

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo -e "${RED}❌ Error: Backend directory not found.${NC}"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: Frontend directory not found.${NC}"
    exit 1
fi

# Start servers
start_backend
start_frontend

# Show status and open browser
show_status
open_browser

# Keep script running
echo -e "${CYAN}🔄 Monitoring servers... (Press Ctrl+C to stop)${NC}"
while true; do
    sleep 10
    # Check if servers are still running
    if ! check_port 8001; then
        echo -e "${RED}❌ Backend server stopped unexpectedly${NC}"
    fi
    if ! check_port 3000; then
        echo -e "${RED}❌ Frontend server stopped unexpectedly${NC}"
    fi
done 