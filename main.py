from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import get_answer
from mcp import generate_mcp
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Define the request schema
class QueryRequest(BaseModel):
    user_id: str
    question: str

# POST endpoint for /query
@app.post("/query")
def query_endpoint(query: QueryRequest):
    request_id = str(uuid.uuid4())

    # Step 1: Run the RAG engine to get an answer + list of document IDs
    answer, doc_ids = get_answer(query.question)

    # Step 2: Generate metadata payload (MCP format)
    mcp_payload = generate_mcp(
        request_id=request_id,
        user_id=query.user_id,
        query=query.question,
        doc_ids=doc_ids
    )

    # Step 3: Return the answer and metadata to the user
    return {
        "answer": answer,
        "metadata": mcp_payload
    }
