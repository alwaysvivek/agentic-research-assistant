import os
import lancedb
from typing import List, TypedDict, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# Load env variables
load_dotenv()

# --- Configuration & Setup ---
# We use an absolute path or relative to the running container/app for data
DB_URI = os.path.join(os.getcwd(), "data/lancedb")
EMBEDDING_MODEL = "models/text-embedding-004"
LLM_MODEL = "gemini-flash-latest"

class Answer(BaseModel):
    answer: str = Field(description="The answer to the user's question.")
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0.")
    source_chunk_ids: List[str] = Field(description="List of chunk IDs used for the answer.")

class ResearchState(TypedDict):
    query: str
    documents: List[Document]
    answer: Optional[Answer]
    try_count: int

# --- Ingestion ---
def load_data(source: str) -> List[Document]:
    """Loads data from a URL or local PDF."""
    documents = []
    if source.startswith("http"):
        print(f"Loading URL: {source}")
        loader = WebBaseLoader(source)
        documents.extend(loader.load())
    elif source.endswith(".pdf"):
        print(f"Loading PDF: {source}")
        loader = PyPDFLoader(source)
        documents.extend(loader.load())
    return documents

def split_text(documents: List[Document]) -> List[Document]:
    """Splits documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def index_text(text: str):
    """Indexes raw text directly."""
    docs = [Document(page_content=text, metadata={"source": "raw_text"})]
    chunks = split_text(docs)
    return index_documents(chunks)

# --- Vector Store (LanceDB) ---
def get_vector_store():
    # Ensure directory exists
    os.makedirs(DB_URI, exist_ok=True)
    db = lancedb.connect(DB_URI)
    return db

def index_documents(chunks: List[Document]):
    """Indexes documents into LanceDB."""
    # sanitize metadata to avoid schema conflicts (e.g. PDF author field)
    for chunk in chunks:
        # Only keep 'source' in metadata, remove everything else
        source = chunk.metadata.get("source", "unknown")
        chunk.metadata = {"source": source}

    # Ensure we use embeddings wrapper compatible with LangChain
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    from langchain_community.vectorstores import LanceDB
    
    vector_store = LanceDB.from_documents(
        documents=chunks,
        embedding=embeddings,
        uri=DB_URI,
        table_name="research_docs"
    )
    return vector_store


def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    from langchain_community.vectorstores import LanceDB
    vector_store = LanceDB(
        uri=DB_URI,
        embedding=embeddings,
        table_name="research_docs"
    )
    return vector_store.as_retriever()


# --- Logic (Graph Nodes) ---
def node_retrieve_and_generate(state: ResearchState):
    query = state["query"]
    print(f"--- Retrieve & Generate for: {query} ---")
    
    retriever = get_retriever()
    docs = retriever.invoke(query)
    
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(Answer)
    
    context_text = "\n\n".join([d.page_content for d in docs])
    prompt = ChatPromptTemplate.from_template(
        """You are a reliable researcher. Answer the question based ONLY on the following context.
        If you cannot find the answer in the context, set output confidence_score to 0.0.
        
        Context:
        {context}
        
        Question: {question}
        """
    )
    chain = prompt | structured_llm
    response = chain.invoke({"context": context_text, "question": query})
    
    return {"answer": response, "documents": docs, "try_count": state.get("try_count", 0) + 1}

def node_grade(state: ResearchState):
    answer = state["answer"]
    if answer.confidence_score > 0.7:
        return "end"
    if state["try_count"] >= 3:
        return "end"
    return "retry"

def build_graph():
    builder = StateGraph(ResearchState)
    builder.add_node("retrieve_and_generate", node_retrieve_and_generate)
    builder.set_entry_point("retrieve_and_generate")
    
    builder.add_conditional_edges(
        "retrieve_and_generate",
        node_grade,
        {
            "end": END,
            "retry": "retrieve_and_generate"
        }
    )
    return builder.compile()

# Helper for async execution if needed, but synchronous invoke is fine for first pass
def run_research(query: str):
    graph = build_graph()
    result = graph.invoke({"query": query, "try_count": 0})
    return result
