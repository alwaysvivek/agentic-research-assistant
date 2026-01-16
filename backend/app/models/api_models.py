from pydantic import BaseModel

class IngestRequest(BaseModel):
    source: str

class IngestTextRequest(BaseModel):
    text: str

class IngestResponse(BaseModel):
    status: str
    message: str
    chunks_count: int

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    answer: str
    confidence_score: float
    source_chunk_ids: list[str]
