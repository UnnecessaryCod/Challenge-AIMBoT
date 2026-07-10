"""
Pruebas básicas del flujo RAG (sin llamadas a APIs externas).
Cubren carga documental, exclusión de documentos internos, chunking,
inferencia de categoría, prompt de AimBot y mensajes de fallback.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import settings
from src.ingestion.document_loader import (
    EXCLUDED_SOURCES,
    chunk_documents,
    infer_category,
    load_markdown_documents,
)
from src.prompts.aimbot_prompt import (
    FALLBACK_MESSAGE,
    FALLBACK_RESPONSE,
    build_prompt,
)


def test_load_markdown_documents_excludes_internal():
    documents = load_markdown_documents()
    assert len(documents) >= 7, "La base comercial debe estar en data/raw"
    sources = {doc["metadata"]["source"] for doc in documents}
    assert not sources & EXCLUDED_SOURCES, "Los documentos internos no deben cargarse"
    for doc in documents:
        assert doc["content"].strip()
        assert doc["metadata"]["source"].endswith(".md")
        assert doc["metadata"]["category"]


def test_load_markdown_documents_include_internal_flag():
    documents = load_markdown_documents(include_internal=True)
    sources = {doc["metadata"]["source"] for doc in documents}
    assert EXCLUDED_SOURCES <= sources, "Con include_internal deben cargarse todos"


def test_excluded_sources_are_the_internal_docs():
    assert EXCLUDED_SOURCES == {
        "00_readme_base_conocimiento.md",
        "02_aimbot_comportamiento.md",
        "09_matriz_documental_limpia.md",
    }


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
        assert meta["source"] not in EXCLUDED_SOURCES
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
    assert FALLBACK_MESSAGE in prompt


def test_fallback_messages():
    assert FALLBACK_MESSAGE == (
        "No encontré información suficiente en la base documental disponible "
        "para responder con precisión."
    )
    # El fallback orientador no debe mencionar documentos internos
    assert ".md" not in FALLBACK_RESPONSE
    assert "Executive Search" in FALLBACK_RESPONSE
    assert "¿Tu necesidad está relacionada" in FALLBACK_RESPONSE


def test_settings_defaults():
    assert settings.TOP_K >= 1
    assert settings.CHUNK_SIZE > settings.CHUNK_OVERLAP
    assert settings.MODEL_PROVIDER in ("openai", "gemini", "cohere")
