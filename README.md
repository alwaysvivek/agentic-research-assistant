# Reliable Researcher - Fullstack AI Application

A production-grade Agentic RAG application that researches topics by ingesting content (URLs/PDFs) and using a self-correcting LangGraph workflow to generate reliable answers.

## Features
- **Fullstack Architecture**: FastAPI Backend + React/Vite Frontend.
- **Agentic Workflow**: Uses LangGraph for Retrieve-Grade-Generate loops.
- **Local Vector DB**: LanceDB for efficient, serverless embedding storage.
- **Beautiful UI**: Modern, responsive interface built with Tailwind CSS.

## Structure
- `backend/`: FastAPI application handling ingestion, RAG, and Agent logic.
- `frontend/`: React application for user interaction.
- `course_archive/`: Archived course materials.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google API Key (in `.env`)

### 1. Backend Setup
```bash
cd backend
pip install -r pyproject.toml # or install dependencies manually
# Ensure .env is present in root or backend with GOOGLE_API_KEY
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) to use the app.
