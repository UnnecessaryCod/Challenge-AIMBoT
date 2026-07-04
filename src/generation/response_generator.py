"""
Generación de respuestas de AimBot con base en el contexto recuperado.
Incluye fallback cuando no hay evidencia documental suficiente.
"""

from src.config.providers import generate_text
from src.prompts.aimbot_prompt import FALLBACK_MESSAGE, build_prompt
from src.retrieval.vector_store import retrieve_context


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
        return {"answer": FALLBACK_MESSAGE, "sources": [], "used_fallback": True}

    chunks = retrieve_context(question)
    if not chunks:
        return {"answer": FALLBACK_MESSAGE, "sources": [], "used_fallback": True}

    answer = generate_text(build_prompt(question, chunks))

    # Fuentes únicas conservando el orden de relevancia
    sources = []
    seen = set()
    for chunk in chunks:
        meta = chunk["metadata"]
        key = meta.get("source", "")
        if key and key not in seen:
            seen.add(key)
            sources.append({"source": key, "category": meta.get("category", "")})

    used_fallback = FALLBACK_MESSAGE[:60].lower() in answer.lower()
    return {
        "answer": answer,
        "sources": [] if used_fallback else sources,
        "used_fallback": used_fallback,
    }
