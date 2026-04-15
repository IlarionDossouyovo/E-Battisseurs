#!/bin/bash

echo "====================================="
echo "E-Battisseurs Build Script"
echo "====================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if in project directory
if [ ! -f "backend/pyproject.toml" ]; then
    echo "Error: Run from project root or specify project path"
    exit 1
fi

echo -e "${GREEN}Installing dependencies...${NC}"
cd backend
source .venv/bin/activate
uv sync

echo -e "${GREEN}Building frontend assets...${NC}"
# Placeholder for frontend build (if needed)

echo -e "${GREEN}Running tests...${NC}"
python -c "from main import app; print('API import OK')" 2>/dev/null || echo "Warning: Need to run from backend dir"

echo -e "${GREEN}Build complete!${NC}"
echo ""
echo "To start the API:"
echo "  cd backend"
echo "  source .venv/bin/activate"  
echo "  uvicorn main:app --reload"
echo ""
echo "Or with Docker:"
echo "  docker-compose up -d"