"""
Base vectorial local con ChromaDB.
Crea, persiste, reutiliza y reconstruye el índice de la base limpia,
y expone la búsqueda semántica para el flujo RAG.
"""

from pathlib import Path

import chromadb

from src.config import settings
from src.config.providers import ProviderError, embed_query, embed_texts
from src.ingestion.document_loader import chunk_documents, load_markdown_documents


def _client() -> chromadb.PersistentClient:
    Path(settings.VECTOR_DB_PATH).mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)


def _get_collection(client: chromadb.PersistentClient):
    return client.get_or_create_collection(
        name=settings.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def vector_store_exists() -> bool:
    """Indica si ya existe un índice persistido con contenido."""
    try:
        collection = _get_collection(_client())
        return collection.count() > 0
    except Exception:
        return False


def build_vector_store(rebuild: bool = False) -> int:
    """
    Crea (o reconstruye) el índice vectorial desde data/raw.
    Devuelve la cantidad de chunks indexados.
    """
    documents = load_markdown_documents()
    if not documents:
        raise ProviderError(
            f"No se encontraron documentos Markdown en '{settings.DOCUMENTS_PATH}'. "
            "Verifica la base documental limpia."
        )

    chunks = chunk_documents(documents)
    texts = [chunk["content"] for chunk in chunks]

    client = _client()
    if rebuild:
        try:
            client.delete_collection(settings.COLLECTION_NAME)
        except Exception:
            pass

    collection = _get_collection(client)
    if not rebuild and collection.count() > 0:
        return collection.count()

    embeddings = embed_texts(texts)
    collection.add(
        ids=[f"{c['metadata']['source']}::{c['metadata']['chunk_number']}" for c in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[chunk["metadata"] for chunk in chunks],
    )
    return collection.count()


def retrieve_context(question: str, top_k: int | None = None) -> list[dict]:
    """
    Devuelve los fragmentos más relevantes para la pregunta.
    Filtra por distancia coseno máxima (settings.MAX_DISTANCE) para
    evitar respuestas fuera del alcance documental.
    """
    top_k = top_k or settings.TOP_K
    collection = _get_collection(_client())
    if collection.count() == 0:
        return []

    query_embedding = embed_query(question)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for text, metadata, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        if distance <= settings.MAX_DISTANCE:
            chunks.append({"content": text, "metadata": metadata, "distance": distance})
    return chunks
