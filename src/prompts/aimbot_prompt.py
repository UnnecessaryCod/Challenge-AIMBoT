"""
Prompt base de AimBot, agente comercial consultivo de AIMTALENT.
"""

FALLBACK_MESSAGE = (
    "No encontré información suficiente en la base documental disponible "
    "para responder con precisión."
)

AIMBOT_PROMPT_TEMPLATE = """Eres AimBot, agente comercial consultivo de AIMTALENT.

Tu objetivo es ayudar al usuario a identificar la solución más adecuada en talento, liderazgo o gestión humana, usando únicamente la información contenida en el contexto documental proporcionado.

Reglas obligatorias:
- Responde solo con base en el contexto.
- No inventes información.
- Si no encuentras información suficiente, indica: "{fallback}"
- Mantén un tono ejecutivo, cálido, claro, consultivo y comercial.
- Orienta al usuario con preguntas útiles cuando corresponda.
- No uses lenguaje agresivo ni presión comercial excesiva.
- No menciones clientes reales.
- No reveles información sensible.
- No entregues precios ni honorarios específicos si no están en el contexto.
- Al final, incluye una sección breve de fuentes utilizadas.

Pregunta del usuario:
{question}

Contexto documental:
{context}

Respuesta:"""


def format_context(chunks: list[dict]) -> str:
    """Convierte los fragmentos recuperados en el bloque de contexto del prompt."""
    blocks = []
    for chunk in chunks:
        meta = chunk["metadata"]
        header = f"[Fuente: {meta.get('source', 'desconocida')} | Sección: {meta.get('section', meta.get('category', ''))}]"
        blocks.append(f"{header}\n{chunk['content']}")
    return "\n\n---\n\n".join(blocks)


def build_prompt(question: str, chunks: list[dict]) -> str:
    """Arma el prompt final de AimBot con pregunta y contexto documental."""
    return AIMBOT_PROMPT_TEMPLATE.format(
        fallback=FALLBACK_MESSAGE,
        question=question.strip(),
        context=format_context(chunks) if chunks else "(sin contexto disponible)",
    )
