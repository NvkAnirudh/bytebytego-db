"""
ByteByteGo RAG System

A Retrieval-Augmented Generation system for intelligent Q&A over ByteByteGo articles.
"""

__version__ = "0.1.0"

from bbgodb.core import settings
from bbgodb.generation import LLMService
from bbgodb.retrieval import EmbeddingService, HybridRetriever

__all__ = [
    "settings",
    "EmbeddingService",
    "HybridRetriever",
    "LLMService",
]
