#!/bin/bash
# Quick start script for the "Build Once, Deploy Many" example

set -e

echo "================================"
echo "Build Once, Deploy Many Example"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "Error: Node.js/npm is required but not installed."
    exit 1
fi

echo -e "${GREEN}✓ Python and npm found${NC}"
echo ""

# Install backend dependencies
echo -e "${BLUE}Installing backend dependencies...${NC}"
cd backend
pip install -q -r requirements.txt
cd ..
echo -e "${GREEN}✓ Backend dependencies installed${NC}"
echo ""

# Install frontend dependencies
echo -e "${BLUE}Installing frontend dependencies...${NC}"
cd frontend
npm install --quiet
cd ..
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
echo ""

echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1. Start the backend (in one terminal):"
echo "   cd backend"
echo "   python main.py"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open http://localhost:5173 in your browser"
echo ""
echo -e "${BLUE}To demonstrate runtime configuration:${NC}"
echo ""
echo "   1. Edit frontend/public/config.json to change BACKEND_URL"
echo "   2. Reload the app - no rebuild needed!"
echo ""
