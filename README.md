# ByteByteGo RAG System

A Retrieval-Augmented Generation (RAG) system that provides intelligent Q&A capabilities over ByteByteGo substack articles. Query system design concepts, architecture patterns, and technical knowledge with AI-powered answers backed by authoritative sources.

## Features

- **Intelligent Q&A**: Ask questions about system design and get comprehensive answers with source citations
- **Multimodal Support**: Process both text AND images from articles using LlamaIndex
  - Automatic image extraction from ByteByteGo articles
  - AI-generated descriptions of architecture diagrams
  - Image-aware retrieval (find relevant diagrams for your queries)
- **Semantic Search**: Advanced vector-based retrieval finds relevant content across all ByteByteGo articles
- **Streaming Responses**: Real-time answer generation for better user experience
- **Multi-LLM Support**: Works with OpenAI GPT-4, GPT-4 Vision, and Anthropic Claude
- **LlamaIndex Integration**: Built-in RSS readers and multimodal capabilities
- **Observability**: Built-in tracing and metrics with LangSmith integration
- **REST API**: FastAPI-based API with OpenAPI documentation
- **CLI Tools**: Command-line interface for ingestion and management

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system architecture and design decisions.

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 6+
- OpenAI API key
- Pinecone account (free tier available)

### Setup

1. **Clone and create virtual environment**:
```bash
uv venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

2. **Install dependencies**:
```bash
uv pip install -e .
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY
# - PINECONE_API_KEY
# - PINECONE_ENVIRONMENT
# - DATABASE_URL
# - etc.
```

4. **Start infrastructure** (using Docker Compose):
```bash
docker-compose up -d postgres redis
```

5. **Initialize database**:
```bash
python -m bbgodb.cli init
```

6. **Ingest ByteByteGo articles**:
```bash
# Default: LlamaIndex pipeline with multimodal support (text + images)
python -m bbgodb.cli ingest

# Or legacy text-only pipeline
python -m bbgodb.cli ingest --no-use-llamaindex
```

**Note**: With LlamaIndex multimodal support enabled, the system will:
- Extract text content from RSS feeds
- Download and process images from articles
- Generate AI descriptions of diagrams using GPT-4 Vision
- Store both text and image embeddings

See [LLAMAINDEX_GUIDE.md](LLAMAINDEX_GUIDE.md) for detailed information about multimodal features.

7. **Start API server**:
```bash
python -m bbgodb.cli serve
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation.

## Usage

### Using the API

**Query endpoint** (basic):
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does consistent hashing work?",
    "top_k": 5,
    "include_sources": true
  }'
```

**Streaming endpoint**:
```bash
curl -X POST http://localhost:8000/api/v1/query/stream \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the CAP theorem",
    "top_k": 5
  }'
```

**List articles**:
```bash
curl http://localhost:8000/api/v1/articles?limit=20
```

**Get system stats**:
```bash
curl http://localhost:8000/api/v1/stats
```

### Using the CLI

**Initialize database**:
```bash
python -m bbgodb.cli init
```

**Ingest all articles from RSS**:
```bash
python -m bbgodb.cli ingest
```

**Ingest single article**:
```bash
python -m bbgodb.cli ingest-url "https://blog.bytebytego.com/p/article-url"
```

**Show statistics**:
```bash
python -m bbgodb.cli stats
```

**Start API server**:
```bash
python -m bbgodb.cli serve
```

### Python SDK

```python
import asyncio
from bbgodb.retrieval import EmbeddingService, HybridRetriever
from bbgodb.generation import LLMService
from bbgodb.utils import AsyncSessionLocal

async def query_example():
    async with AsyncSessionLocal() as db:
        # Initialize services
        embedding_service = EmbeddingService()
        retriever = HybridRetriever(db, embedding_service)
        llm_service = LLMService()

        # Retrieve relevant sources
        sources = await retriever.retrieve("How does load balancing work?", top_k=5)

        # Generate answer
        answer, tokens = await llm_service.generate_response(
            "How does load balancing work?",
            sources
        )

        print(f"Answer: {answer}")
        print(f"Tokens used: {tokens}")
        print(f"Sources: {len(sources)}")

asyncio.run(query_example())
```

## Project Structure

```
bbgodb/
├── src/bbgodb/
│   ├── api/              # FastAPI application and routes
│   ├── core/             # Configuration and settings
│   ├── ingestion/        # Data ingestion pipeline
│   │   ├── scraper.py    # ByteByteGo article scraping
│   │   ├── chunker.py    # Text chunking logic
│   │   └── pipeline.py   # Orchestration
│   ├── retrieval/        # Retrieval components
│   │   ├── embeddings.py # Embedding generation and vector search
│   │   └── retriever.py  # Hybrid retrieval logic
│   ├── generation/       # LLM response generation
│   │   └── llm.py        # OpenAI/Anthropic integration
│   ├── observability/    # Tracing and metrics
│   ├── models/           # Pydantic and SQLAlchemy models
│   ├── utils/            # Database and utilities
│   └── cli.py            # CLI interface
├── ARCHITECTURE.md       # Detailed architecture docs
├── docker-compose.yml    # Docker services
├── Dockerfile            # API container
└── pyproject.toml        # Dependencies
```

## Development

### Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

### Run tests:
```bash
pytest
```

### Code formatting:
```bash
black src/
ruff check src/
```

### Type checking:
```bash
mypy src/
```

## Docker Deployment

### Full stack with Docker Compose:
```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- Redis cache
- API server

### Build custom image:
```bash
docker build -t bbgodb:latest .
```

## Configuration

All configuration is managed through environment variables. See `.env.example` for all available options.

### Key Settings

- `OPENAI_API_KEY`: OpenAI API key for embeddings and generation
- `ANTHROPIC_API_KEY`: (Optional) Anthropic API key for Claude
- `PINECONE_API_KEY`: Pinecone API key for vector storage
- `PINECONE_ENVIRONMENT`: Pinecone environment (e.g., "us-west1-gcp")
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `LANGCHAIN_API_KEY`: (Optional) LangSmith API key for tracing

## Monitoring and Observability

The system includes built-in observability:

- **LangSmith Integration**: Automatic tracing of LLM calls and retrieval
- **Metrics Collection**: Latency, token usage, error rates
- **API Metrics**: Available at `/api/v1/stats`

## Performance

- **Query Latency**: ~1-3 seconds (p95)
- **Retrieval**: ~200-500ms for top-10 results
- **Generation**: ~1-2 seconds for GPT-4 responses
- **Throughput**: ~10-20 concurrent requests (single instance)

## Roadmap

- [ ] Re-ranking with cross-encoders
- [ ] Multi-modal support (diagrams, images)
- [ ] Conversation memory
- [ ] User feedback collection
- [ ] Fine-tuned domain models
- [ ] Real-time article updates
- [ ] Advanced caching strategies

## Contributing

Contributions welcome! Please open an issue first to discuss proposed changes.

## License

MIT License - see LICENSE file for details.

## Key Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System architecture and design decisions
- **[LLAMAINDEX_GUIDE.md](LLAMAINDEX_GUIDE.md)**: LlamaIndex integration and multimodal features
- **[GETTING_STARTED.md](GETTING_STARTED.md)**: Step-by-step setup guide

## Acknowledgments

Built with:
- [LlamaIndex](https://www.llamaindex.ai/) - Data framework for LLM applications
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [OpenAI](https://openai.com/) - Embeddings, GPT-4, and Vision API
- [Pinecone](https://www.pinecone.io/) - Vector database
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit

Inspired by ByteByteGo's excellent system design content.
