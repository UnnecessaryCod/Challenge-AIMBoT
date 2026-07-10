"""
Generación de respuestas de AimBot con base en el contexto recuperado.
Filtra documentos internos de las fuentes y aplica fallback orientador
cuando no hay evidencia documental suficiente.
"""

from src.config.providers import generate_text
from src.ingestion.document_loader import EXCLUDED_SOURCES
from src.prompts.aimbot_prompt import FALLBACK_MESSAGE, FALLBACK_RESPONSE, build_prompt
from src.retrieval.vector_store import retrieve_context

_FALLBACK_RESULT = {"answer": FALLBACK_RESPONSE, "sources": [], "used_fallback": True}


def generate_response(question: str) -> dict:
    """
    Ejecuta retrieval + LLM y devuelve la respuesta con fuentes.

    Retorna:
        {
            "answer": str,
            "sources": [{"source": str, "category": str}],
            "used_fallback": bool,
        }
    """
    question = (question or "").strip()
    if not question:
        return dict(_FALLBACK_RESULT)

    chunks = retrieve_context(question)
    # Defensa adicional: nunca usar documentos internos como contexto ni fuente,
    # incluso si un índice antiguo todavía los contiene.
    chunks = [c for c in chunks if c["metadata"].get("source") not in EXCLUDED_SOURCES]
    if not chunks:
        return dict(_FALLBACK_RESULT)

    answer = generate_text(build_prompt(question, chunks))

    # Si el modelo declara falta de evidencia, mostrar el fallback orientador sin fuentes.
    if FALLBACK_MESSAGE[:60].lower() in answer.lower():
        return dict(_FALLBACK_RESULT)

    # Fuentes únicas conservando el orden de relevancia
    sources = []
    seen = set()
    for chunk in chunks:
        meta = chunk["metadata"]
        key = meta.get("source", "")
        if key and key not in seen:
            seen.add(key)
            sources.append({"source": key, "category": meta.get("category", "")})

    return {"answer": answer, "sources": sources, "used_fallback": False}
