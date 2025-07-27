📦 ragstack-gpt-observability
A production-grade Retrieval-Augmented Generation (RAG) system powered by OpenAI's GPT-4, Kafka-based metadata logging, and observability using Prometheus and Grafana. Built with FastAPI, LangChain, and ChromaDB, this project serves as an intelligent query engine that combines LLM capabilities with your private data and full-stack monitoring.

🚀 Features Implemented

👉 1. LLM-Powered Query Engine (FastAPI + GPT-4)

Built with FastAPI to expose a /query endpoint

Accepts user input and generates intelligent answers using OpenAI’s GPT-4

Integrated with LangChain for prompt templating and inference orchestration

👉 2. Retrieval-Augmented Generation (RAG)

Stores private documents in Chroma vector database

Retrieves top-k relevant chunks, augments the query, and forwards it to GPT-4

Uses OpenAIEmbeddings for vectorization and similarity search

👉 3. RAG Engine (rag_engine.py)

Executes the full pipeline: embeddings → retrieval → prompt assembly → GPT call

Returns both the answer and the document IDs used

Environment-driven configuration (e.g., top-k, model version)

👉 4. Metadata Control Protocol (MCP)

Wraps each query with structured metadata including:

request_id, user_id, timestamp

document_ids, prompt version, model version

Centralized logic in mcp.py

👉 5. Kafka Integration for Query Events

kafka_producer.py emits query metadata to a Kafka topic: query-events

Enables downstream systems to log, trace, or react to user queries

Fully decouples analytics from the application logic

👉 6. Requirements & Dependency Management

requirements.txt defines all Python dependencies

python-dotenv used to manage environment variables

👉 7. Production-Ready Project Layout

Modular backend structure

Environment variable-driven configuration using .env.example

Supports Docker, Kubernetes, and ArgoCD deployment strategies

📁 Folder Structure

llm-rag-app/
├── backend/
│   ├── main.py              # FastAPI app & /query endpoint
│   ├── rag_engine.py        # Executes RAG pipeline
│   ├── mcp.py               # Metadata packaging
│   ├── kafka_producer.py    # Kafka publisher for events
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Sample environment variables
├── deploy/
│   ├── docker-compose.yml   # (upcoming) Local test stack
│   ├── helm/                # (planned) Kubernetes Helm Charts
│   └── argocd/              # (planned) ArgoCD GitOps config
└── README.md

🧠 Tech Stack

OpenAI GPT-4 (LLM inference)

LangChain (RAG orchestration)

ChromaDB (vector similarity DB)

FastAPI (web server framework)

Kafka (message broker for query metadata)

Prometheus + Grafana (observability)

Loki (future: logging)

Docker, Kubernetes, ArgoCD (infrastructure)

🔬 Example Query Flow

User sends POST to /query with: “What is Retrieval-Augmented Generation?”

FastAPI app calls rag_engine.get_answer()

Question is embedded

ChromaDB retrieves relevant chunks

Prompt is constructed and sent to OpenAI (GPT-4)

GPT-4 response is returned

MCP metadata is generated

Kafka producer publishes metadata to topic query-events