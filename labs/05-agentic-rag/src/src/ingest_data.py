import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Configuration
project_root = Path(__file__).parent.parent.parent.parent
docs_dir = project_root / "crewAI" / "chapter3" / "data" / "docs"
db_dir = project_root / "crewAI" / "chapter3" / "data" / "chroma_db"

def ingest():
    """
    Ingests local documents into a vector database for Agentic RAG.
    """
    print(f"📥 Loading documents from {docs_dir}...")
    
    if not docs_dir.exists():
        print(f"❌ Documents directory {docs_dir} does not exist.")
        return

    # 1. Load Documents (Markdown and Text)
    loader = DirectoryLoader(str(docs_dir), glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("⚠️ No documents found to ingest.")
        return

    # 2. Split into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50
    )
    texts = text_splitter.split_documents(documents)
    print(f"✂️ Split into {len(texts)} chunks.")

    # 3. Initialize local embeddings
    # Using 'nomic-embed-text' via Ollama for sovereign privacy
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 4. Create and Persist Chroma Vector DB
    print(f"💾 Creating local ChromaDB at {db_dir}...")
    
    # We clear the existing DB if any to ensure a clean start for this chapter
    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=str(db_dir),
        collection_name="sovereign_knowledge"
    )
    
    print(f"✅ Ingestion complete! Knowledge base is ready for Agentic RAG.")

if __name__ == "__main__":
    ingest()
