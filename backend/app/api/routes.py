from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.api_models import IngestRequest, IngestResponse, ResearchRequest, ResearchResponse, IngestTextRequest
from app.services.researcher import load_data, split_text, index_documents, run_research, index_text
import shutil
import os
import traceback

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_endpoint(request: IngestRequest):
    try:
        # 1. Load
        docs = load_data(request.source)
        if not docs:
            raise HTTPException(status_code=400, detail="Could not load data from source.")
        
        # 2. Split
        chunks = split_text(docs)
        
        # 3. Index
        index_documents(chunks)
        
        return IngestResponse(
            status="success", 
            message=f"Successfully ingested {request.source}",
            chunks_count=len(chunks)
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest/text", response_model=IngestResponse)
async def ingest_text_endpoint(request: IngestTextRequest):
    try:
        index_text(request.text)
        return IngestResponse(
            status="success",
            message="Successfully ingested raw text.",
            chunks_count=1 # Approximate
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest/file", response_model=IngestResponse)
async def ingest_file_endpoint(file: UploadFile = File(...)):
    try:
        # Save temp file
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Load and Index
        docs = load_data(temp_path)
        chunks = split_text(docs)
        index_documents(chunks)
        
        # Cleanup
        os.remove(temp_path)
        
        return IngestResponse(
            status="success",
            message=f"Successfully ingested {file.filename}",
            chunks_count=len(chunks)
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/research", response_model=ResearchResponse)
async def research_endpoint(request: ResearchRequest):
    try:
        # Run LangGraph workflow
        result = run_research(request.query)
        answer_obj = result.get("answer")
        
        if not answer_obj:
             raise HTTPException(status_code=404, detail="No answer found.")

        return ResearchResponse(
            answer=answer_obj.answer,
            confidence_score=answer_obj.confidence_score,
            source_chunk_ids=answer_obj.source_chunk_ids
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
