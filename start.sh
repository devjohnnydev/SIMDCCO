#!/bin/bash

# SIMDCCO Quick Start Script
# This script sets up and runs both backend and frontend

set -e

echo "🚀 SIMDCCO Quick Start"
echo "======================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in SIMDCCO directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the SIMDCCO root directory"
    exit 1
fi

echo "📦 Step 1: Setting up Backend..."
cd backend

# Detect Python command
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    # In Docker, we know it's there, but let's be safe
    PYTHON_CMD=$(which python3 || which python)
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python not found. Please install Python."
    exit 1
fi
echo "Using Python command: $PYTHON_CMD"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "${YELLOW}⚠️  No .env file found. Creating from example...${NC}"
    cp .env.example .env
fi

# Run database seed
echo "Initializing database and seeding data..."
$PYTHON_CMD seed.py

# Start backend in background
BACKEND_PORT=8000
echo "Starting backend server on port 127.0.0.1:$BACKEND_PORT..."
uvicorn app.main:app --host 127.0.0.1 --port $BACKEND_PORT &
BACKEND_PID=$!
echo "${GREEN}✅ Backend running on http://127.0.0.1:$BACKEND_PORT${NC}"
echo "   API Docs: http://127.0.0.1:8000/api/docs"

cd ..

echo ""
echo "📦 Step 2: Setting up Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local..."
    cp .env.local.example .env.local
fi

# Start frontend
echo "Starting frontend server..."
export PORT=${PORT:-3000}
if [ "$NIXPACKS_PHASE" = "start" ] || [ -n "$RAILWAY_ENVIRONMENT" ]; then
    npm run start &
else
    npm run dev &
fi
FRONTEND_PID=$!

echo "${GREEN}✅ Frontend running${NC}"

cd ..

echo ""
echo "════════════════════════════════════"
echo "${GREEN}✨ SIMDCCO is now running!${NC}"
echo "════════════════════════════════════"
echo ""
echo "📍 URLs:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend:  http://localhost:8000"
echo "   • API Docs: http://localhost:8000/api/docs"
echo ""
echo "🔑 Default Admin Credentials:"
echo "   • Email:    admin@simdcco.com"
echo "   • Password: admin123"
echo "   ${YELLOW}⚠️  CHANGE PASSWORD IN PRODUCTION!${NC}"
echo ""
echo "📋 Next Steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Test the respondent flow"
echo "   3. Login to admin panel"
echo ""
echo "Press Ctrl+C to stop all servers..."
echo ""

# Wait for interrupt
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '${GREEN}✅ Servers stopped${NC}'; exit 0" INT

# Keep script running
wait
