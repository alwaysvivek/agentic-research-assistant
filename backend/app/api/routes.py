from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.models.api_models import IngestRequest, IngestResponse, ResearchRequest, ResearchResponse, IngestTextRequest
from app.services.researcher import load_data, split_text, index_documents, run_research, index_text
import shutil
import os
import traceback
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
@limiter.limit("10/minute")
async def ingest_endpoint(request: IngestRequest, req: Request):
    """Ingest content from URL or PDF file path"""
    try:
        # Validate source
        if not request.source or not request.source.strip():
            raise HTTPException(status_code=400, detail="Source URL or file path is required")
        
        source = request.source.strip()
        
        # Validate URL or file format
        if not (source.startswith("http://") or source.startswith("https://") or source.endswith(".pdf")):
            raise HTTPException(
                status_code=400,
                detail="Source must be a valid HTTP(S) URL or PDF file path"
            )
        
        logger.info(f"Ingesting from source: {source}")
        
        # 1. Load
        docs = load_data(source)
        if not docs:
            raise HTTPException(
                status_code=400,
                detail="Could not load data from source. Please check the URL or file path."
            )
        
        # 2. Split
        chunks = split_text(docs)
        
        # 3. Index
        index_documents(chunks)
        
        logger.info(f"Successfully ingested {len(chunks)} chunks from {source}")
        
        return IngestResponse(
            status="success", 
            message=f"Successfully ingested {source}",
            chunks_count=len(chunks)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting source: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest content: {str(e)}"
        )

@router.post("/ingest/text", response_model=IngestResponse)
@limiter.limit("10/minute")
async def ingest_text_endpoint(request: IngestTextRequest, req: Request):
    """Ingest raw text content"""
    try:
        # Validate text
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="Text content is required")
        
        if len(request.text) > 100000:  # 100KB limit
            raise HTTPException(
                status_code=400,
                detail="Text content too large. Maximum 100,000 characters allowed."
            )
        
        logger.info(f"Ingesting raw text ({len(request.text)} characters)")
        
        index_text(request.text)
        
        return IngestResponse(
            status="success",
            message="Successfully ingested raw text.",
            chunks_count=1  # Approximate
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting text: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest text: {str(e)}"
        )

@router.post("/ingest/file", response_model=IngestResponse)
@limiter.limit("5/minute")
async def ingest_file_endpoint(file: UploadFile = File(...), req: Request = None):
    """Upload and ingest a PDF file"""
    temp_path = None
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Check file size (10MB limit)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=400,
                detail="File too large. Maximum size is 10MB."
            )
        
        logger.info(f"Uploading file: {file.filename} ({file_size} bytes)")
        
        # Save temp file
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Load and Index
        docs = load_data(temp_path)
        if not docs:
            raise HTTPException(
                status_code=400,
                detail="Could not extract content from PDF"
            )
        
        chunks = split_text(docs)
        index_documents(chunks)
        
        logger.info(f"Successfully ingested {len(chunks)} chunks from {file.filename}")
        
        return IngestResponse(
            status="success",
            message=f"Successfully ingested {file.filename}",
            chunks_count=len(chunks)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting file: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest file: {str(e)}"
        )
    finally:
        # Cleanup temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file: {str(e)}")

@router.post("/research", response_model=ResearchResponse)
@limiter.limit("10/minute")
async def research_endpoint(request: ResearchRequest, req: Request):
    """Research a query using the agentic RAG workflow"""
    try:
        # Validate query
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query is required")
        
        query = request.query.strip()
        
        if len(query) > 1000:
            raise HTTPException(
                status_code=400,
                detail="Query too long. Maximum 1000 characters allowed."
            )
        
        logger.info(f"Research query: {query[:100]}...")
        
        # Run LangGraph workflow
        result = run_research(query)
        answer_obj = result.get("answer")
        
        if not answer_obj:
            raise HTTPException(
                status_code=404,
                detail="No answer found. Please ensure you have ingested relevant documents first."
            )

        logger.info(f"Research completed with confidence: {answer_obj.confidence_score}")

        return ResearchResponse(
            answer=answer_obj.answer,
            confidence_score=answer_obj.confidence_score,
            source_chunk_ids=answer_obj.source_chunk_ids
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during research: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(e)}"
        )
