"""
Pruebas básicas del flujo RAG (sin llamadas a APIs externas).
Cubren carga documental, chunking, inferencia de categoría y prompt de AimBot.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import settings
from src.ingestion.document_loader import (
    chunk_documents,
    infer_category,
    load_markdown_documents,
)
from src.prompts.aimbot_prompt import FALLBACK_MESSAGE, build_prompt


def test_load_markdown_documents():
    documents = load_markdown_documents()
    assert len(documents) >= 8, "La base documental limpia debe estar en data/raw"
    for doc in documents:
        assert doc["content"].strip()
        assert doc["metadata"]["source"].endswith(".md")
        assert doc["metadata"]["category"]


def test_infer_category():
    assert infer_category("03_executive_search.md") == "Executive Search"
    assert infer_category("04_hiring_solutions.md") == "Hiring Solutions"
    assert infer_category("archivo_nuevo.md") == "Archivo Nuevo"


def test_chunk_documents_respects_size_and_metadata():
    documents = load_markdown_documents()
    chunks = chunk_documents(documents, chunk_size=800, chunk_overlap=100)
    assert chunks, "El chunking debe producir fragmentos"
    for chunk in chunks:
        assert len(chunk["content"]) <= 800
        meta = chunk["metadata"]
        assert meta["source"].endswith(".md")
        assert meta["category"]
        assert meta["chunk_number"] >= 1
        assert "section" in meta


def test_build_prompt_contains_question_and_context():
    chunks = [
        {
            "content": "AIMTALENT ofrece Executive Search.",
            "metadata": {"source": "03_executive_search.md", "section": "Servicio", "category": "Executive Search"},
        }
    ]
    prompt = build_prompt("¿Qué servicios ofrece AIMTALENT?", chunks)
    assert "¿Qué servicios ofrece AIMTALENT?" in prompt
    assert "AIMTALENT ofrece Executive Search." in prompt
    assert "03_executive_search.md" in prompt
    assert FALLBACK_MESSAGE in prompt


def test_fallback_message_matches_expected():
    assert FALLBACK_MESSAGE == (
        "No encontré información suficiente en la base documental disponible "
        "para responder con precisión."
    )


def test_settings_defaults():
    assert settings.TOP_K >= 1
    assert settings.CHUNK_SIZE > settings.CHUNK_OVERLAP
    assert settings.MODEL_PROVIDER in ("openai", "gemini", "cohere")
