#!/bin/bash

# DISCERA Assistant - Launch Script
# This script starts the backend server and frontend development server

echo "🚀 Starting DISCERA - Digital Intelligent System for Comprehensive Exam Review & Assessment"
echo "=================================================================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the DISCERA project root directory"
    echo "Current directory: $(pwd)"
    echo "Script location: $SCRIPT_DIR"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p chroma_db

# Check if ports are available
echo "🔍 Checking port availability..."

if ! check_port 8001; then
    echo "❌ Port 8001 is already in use. Please stop the service using that port."
    exit 1
fi

if ! check_port 3000; then
    echo "⚠️  Port 3000 is in use, trying port 3001..."
    if ! check_port 3001; then
        echo "❌ Both ports 3000 and 3001 are in use. Please free up one of these ports."
        exit 1
    fi
    FRONTEND_PORT=3001
else
    FRONTEND_PORT=3000
fi

# Start backend server
echo "🔧 Starting DISCERA Backend Server (FastAPI) on port 8001..."
echo "📚 API Documentation will be available at: http://localhost:8001/docs"
echo "🔍 Health check: http://localhost:8001/health"

# Start backend in background
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ Backend server started successfully!"
else
    echo "❌ Backend server failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "📦 Frontend not found. Creating basic frontend structure..."
    mkdir -p frontend
    cd frontend
    
    # Create package.json
    cat > package.json << 'EOF'
{
  "name": "discera-frontend",
  "version": "1.0.0",
  "description": "DISCERA Frontend Application",
  "scripts": {
    "dev": "echo 'Frontend not yet implemented. Please implement frontend separately.'",
    "build": "echo 'Frontend not yet implemented.'",
    "start": "echo 'Frontend not yet implemented.'"
  },
  "dependencies": {},
  "devDependencies": {}
}
EOF
    
    cd ..
fi

# Try to start frontend if it's a Next.js project
if [ -f "frontend/package.json" ]; then
    echo "🎨 Starting DISCERA Frontend Server on port $FRONTEND_PORT..."
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        npm install
    fi
    
    # Start frontend in background
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    # Wait a moment for frontend to start
    sleep 5
    
    echo "✅ Frontend server started successfully!"
    echo "🌐 Frontend will be available at: http://localhost:$FRONTEND_PORT"
else
    echo "⚠️  Frontend not yet implemented. Backend is running at http://localhost:8001"
fi

# Open browser
echo "🌐 Opening browser..."
if command -v open > /dev/null; then
    open "http://localhost:8001/docs"
    if [ ! -z "$FRONTEND_PID" ]; then
        sleep 2
        open "http://localhost:$FRONTEND_PORT"
    fi
elif command -v xdg-open > /dev/null; then
    xdg-open "http://localhost:8001/docs"
    if [ ! -z "$FRONTEND_PID" ]; then
        sleep 2
        xdg-open "http://localhost:$FRONTEND_PORT"
    fi
fi

echo ""
echo "🎉 DISCERA is now running!"
echo "=================================================================================="
echo "📚 Backend API: http://localhost:8001"
echo "📖 API Docs: http://localhost:8001/docs"
echo "🔍 Health Check: http://localhost:8001/health"
if [ ! -z "$FRONTEND_PID" ]; then
    echo "🌐 Frontend: http://localhost:$FRONTEND_PORT"
fi
echo ""
echo "🛑 To stop DISCERA, press Ctrl+C"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping DISCERA..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend server stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend server stopped"
    fi
    echo "👋 DISCERA stopped successfully!"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Keep script running
echo "⏳ DISCERA is running. Press Ctrl+C to stop..."
wait 