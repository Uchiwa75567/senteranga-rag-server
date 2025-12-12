#!/bin/bash

# SENTERANGA Local RAG with Gemini API - Startup Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="${SCRIPT_DIR}/.venv"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting SENTERANGA Local RAG with Gemini API...${NC}"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv "$VENV_PATH"
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Check if index exists
if [ ! -f "$SCRIPT_DIR/index_data/faiss_index.bin" ]; then
    echo -e "${RED}❌ Index not found!${NC}"
    echo -e "${YELLOW}Run this first:${NC}"
    echo "  cd $SCRIPT_DIR"
    echo "  source .venv/bin/activate"
    echo "  python index_corpus.py /home/bachir-uchiwa/Bureau/projet3D"
    exit 1
fi

# Load .env if it exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    echo -e "${GREEN}✓ Loading .env configuration${NC}"
    # Filter out comments and empty lines when loading .env
    set -a
    source <(grep -v '^#' "$SCRIPT_DIR/.env" | grep -v '^$')
    set +a
else
    echo -e "${RED}❌ .env file not found!${NC}"
    echo -e "${YELLOW}Create it from .env.example:${NC}"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your GEMINI_API_KEY"
    exit 1
fi

# Check dependencies
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip install -r "$SCRIPT_DIR/requirements.txt" -q
fi

echo -e "${GREEN}✓ Environment ready${NC}"
echo ""
echo -e "${YELLOW}Starting server with Gemini API...${NC}"
echo "  🔗 Local: http://127.0.0.1:8000"
echo "  📊 Health: http://127.0.0.1:8000/health"
echo "  💬 Chat API: POST http://127.0.0.1:8000/chat"
echo "  🤖 LLM: Gemini 2.5 Flash"
echo ""

# Start server
python -m uvicorn server:app --host 127.0.0.1 --port 8000

