# backend/rag_engine.py

import os
from typing import Tuple, List
from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Constants
CHROMA_DB_DIR = "rag_db"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4")
K_RETRIEVE = 3  # number of top documents to retrieve

# Initialize reusable components
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": K_RETRIEVE})
llm = ChatOpenAI(model_name=MODEL_NAME, temperature=0)


def get_answer(question: str) -> Tuple[str, List[str]]:
    """
    Executes the RAG pipeline:
    1. Retrieve top-k relevant documents from Chroma
    2. Run RetrievalQA with GPT-4
    3. Return the answer and document IDs (sources)
    """
    # Step 1: Retrieve documents
    relevant_docs = retriever.get_relevant_documents(question)
    doc_ids = [doc.metadata.get("source", "unknown") for doc in relevant_docs]

    # Step 2: Create custom prompt (optional — use LangChain default if not specified)
    prompt_template = PromptTemplate.from_template(
        "Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    )

    # Step 3: Construct QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )

    # Step 4: Run the chain and return the result
    answer = qa_chain.run(question)

    return answer, doc_ids
