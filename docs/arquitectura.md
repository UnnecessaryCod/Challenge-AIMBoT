# Arquitectura — AIMBOT Knowledge Agent

## Flujo RAG implementado

```text
data/raw/*.md (base limpia)
        ↓  src/ingestion/document_loader.py
Carga con metadata (fuente, categoría) + chunking (sección, nº de chunk)
        ↓  src/config/providers.py
Embeddings (OpenAI / Gemini / Cohere, según .env)
        ↓  src/retrieval/vector_store.py
ChromaDB persistente (data/processed/vector_store, distancia coseno)
        ↓
Pregunta del usuario (app/streamlit_app.py)
        ↓  retrieve_context: Top K + filtro MAX_DISTANCE
Fragmentos relevantes con metadata
        ↓  src/prompts/aimbot_prompt.py
Prompt de AimBot (reglas comerciales y de seguridad documental)
        ↓  src/generation/response_generator.py
LLM → respuesta con fuentes, o fallback si no hay evidencia
```

## Módulos

| Módulo | Responsabilidad |
|---|---|
| `src/config/settings.py` | Variables de entorno con defaults seguros |
| `src/config/providers.py` | Abstracción OpenAI / Gemini / Cohere (embeddings + generación) |
| `src/ingestion/document_loader.py` | Carga Markdown, inferencia de categoría, chunking |
| `src/retrieval/vector_store.py` | Crear, persistir, reconstruir y consultar ChromaDB |
| `src/prompts/aimbot_prompt.py` | Prompt base y formato de contexto con fuentes |
| `src/generation/response_generator.py` | Orquestación retrieval + LLM + fallback |
| `app/streamlit_app.py` | UI con branding AIMTALENT, chat, fuentes, sidebar |

## Decisiones de diseño

- **Sin LangChain**: el flujo se implementa directo con ChromaDB y SDKs oficiales; menos dependencias, más trazabilidad.
- **Documentos internos excluidos**: `00_readme_base_conocimiento.md`, `02_aimbot_comportamiento.md` y `09_matriz_documental_limpia.md` no se indexan ni se muestran como fuentes (son configuración/control, no contenido comercial). Hay un filtro adicional en la generación por si un índice antiguo los contiene.
- **Fallback orientador**: ante preguntas fuera de alcance, AimBot responde sin fuentes y redirige hacia los servicios reales de AIMTALENT.
- **Filtro de relevancia**: fragmentos con distancia coseno > `MAX_DISTANCE` (default 0.75) se descartan; sin fragmentos válidos se activa el fallback sin llamar al LLM.
- **Proveedor conmutables por `.env`**: `MODEL_PROVIDER` y `EMBEDDINGS_PROVIDER`, con imports perezosos para no requerir SDKs no usados.
- **Índice reutilizable**: se persiste en disco y se reconstruye desde el sidebar o al detectar base vacía.

## Principios de diseño

- Base documental limpia y anonimizada.
- Respuestas basadas en fuentes.
- Tono consultivo y comercial.
- Prevención de alucinaciones.
- Simplicidad técnica para MVP.
