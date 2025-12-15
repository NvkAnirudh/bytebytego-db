# ByteByteGo Database (bbgodb) - Architecture & Requirements

## Project Overview
This project aims to build an intelligent knowledge base system for ByteByteGo articles, enabling users to ask questions and receive accurate, source-backed answers derived from the ByteByteGo content library.

## Architecture Phases

### Phase 1: Data Ingestion
The data ingestion pipeline is responsible for collecting and processing ByteByteGo articles:

1. **ByteByteGo Articles Schedule RSS**
   - Subscribe to ByteByteGo's RSS feed for automated article discovery

2. **Daily Sync Airflow**
   - Automated daily synchronization using Apache Airflow
   - Ensures the knowledge base stays current with new content

3. **Content Processing**
   - Extract and process article content
   - Handle text and multimedia elements

4. **Deduplication & Chunking**
   - Remove duplicate content
   - Split articles into manageable chunks for processing

5. **Embeddings Generation (Text + Images)**
   - Generate vector embeddings for textual content
   - Process and embed images from articles

6. **Storage**
   - **Weaviate Vector DB**: Store embeddings for semantic search
   - **Postgres Metadata**: Store article metadata, relationships, and structured data

### Phase 2: Query & Answer
The query phase handles user questions and generates comprehensive answers:

1. **User Question**
   - Accept natural language questions from users

2. **Query Understanding (Reformulate & Classify)**
   - Analyze and reformulate queries for better retrieval
   - Classify query intent and type

3. **Smart Retrieval (Hybrid Search + Re-rank)**
   - Perform hybrid search combining:
     - Vector similarity search in Weaviate
     - Traditional keyword search
   - Re-rank results for relevance

4. **Context Building (Chunks + Citations + Images)**
   - Assemble relevant content chunks
   - Include proper citations and sources
   - Incorporate relevant images

5. **LLM Generation (Answer with Sources)**
   - Use a Large Language Model to generate answers
   - Include source citations in responses

6. **User Answer**
   - Deliver the final answer to the user

7. **Feedback Ratings**
   - Collect user feedback on answer quality
   - Enable continuous improvement

### Phase 3: Observability
Monitoring and continuous improvement layer:

1. **Monitoring (LangSmith / LangSmith)**
   - Track system performance
   - Monitor query patterns and latency

2. **Quality Metrics (RAGAS + User Ratings)**
   - Use RAGAS (Retrieval-Augmented Generation Assessment) framework
   - Incorporate user ratings for quality assessment

3. **Continuous Improvement (Re-train Re-rankert)**
   - Use feedback to retrain re-ranking models
   - Iteratively improve retrieval and answer quality

## Key Technical Components

### Data Storage
- **Weaviate**: Vector database for semantic search capabilities
- **Postgres**: Relational database for metadata and structured data

### Processing Pipeline
- **Airflow**: Orchestration of daily ingestion workflows
- **Chunking Strategy**: Break articles into optimal sizes for embedding and retrieval
- **Deduplication**: Ensure content uniqueness

### Retrieval System
- **Hybrid Search**: Combine vector similarity with traditional search
- **Re-ranking**: Improve result relevance through secondary ranking
- **Context Assembly**: Build comprehensive context from multiple sources

### Quality Assurance
- **RAGAS Metrics**: Automated quality assessment
- **User Feedback Loop**: Continuous learning from user ratings
- **Monitoring**: Real-time system health and performance tracking

## Project Goals
1. Create a comprehensive, searchable knowledge base of ByteByteGo content
2. Enable accurate question-answering with proper source attribution
3. Maintain freshness through automated daily updates
4. Continuously improve answer quality through monitoring and feedback
5. Provide a seamless user experience with fast, relevant responses
