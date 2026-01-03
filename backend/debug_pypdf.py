from langchain_community.document_loaders import PyPDFLoader
import sys

# Create a dummy PDF file (assuming this script might fail if no real PDF, but we just check import first)
try:
    print("Testing PyPDFLoader import...")
    import pypdf
    print(f"pypdf version: {pypdf.__version__}")
    
    # We can't easily create a valid PDF without reportlab, but let's just check if Loader class loads
    loader = PyPDFLoader
    print("PyPDFLoader class loaded successfully.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
