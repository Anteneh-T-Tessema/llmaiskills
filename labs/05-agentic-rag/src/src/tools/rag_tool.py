from typing import Type
from pathlib import Path
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Configuration
project_root = Path(__file__).parent.parent.parent.parent.parent
db_dir = project_root / "crewAI" / "chapter3" / "data" / "chroma_db"

class KnowledgeSearchInput(BaseModel):
    """Input schema for KnowledgeSearchTool."""
    query: str = Field(..., description="The query to search for in the internal knowledge base.")

class KnowledgeSearchTool(BaseTool):
    name: str = "internal_knowledge_search"
    description: str = "Search the internal Sovereign AI policy and procedures. Use this for questions about company protocols, fact-checking standards, and deployment strategies."
    args_schema: Type[BaseModel] = KnowledgeSearchInput

    def _run(self, query: str) -> str:
        # 1. Initialize Embeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # 2. Load Vector DB
        try:
            vector_db = Chroma(
                persist_directory=str(db_dir),
                embedding_function=embeddings,
                collection_name="sovereign_knowledge"
            )
            
            # 3. Perform Similarity Search
            results = vector_db.similarity_search(query, k=3)
            
            # 4. Format Results
            if not results:
                return "No relevant information found in internal knowledge base."
                
            context = "\n---\n".join([res.page_content for res in results])
            return f"Found relevant excerpts from internal knowledge base:\n{context}"
            
        except Exception as e:
            return f"Error searching knowledge base: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    tool = KnowledgeSearchTool()
    print(tool._run("What is the protocol for fact-checking?"))
