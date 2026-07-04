"""
Capa de proveedores de IA (OpenAI, Gemini, Cohere).
Expone dos operaciones: generar texto y calcular embeddings.
Los SDK se importan de forma perezosa para que un proveedor no instalado
no rompa la app si no está seleccionado.
"""

from src.config import settings

SUPPORTED_PROVIDERS = ("openai", "gemini", "cohere")


class ProviderError(Exception):
    """Error amigable de configuración o conexión con el proveedor de IA."""


def _require_key(provider: str) -> str:
    if provider not in SUPPORTED_PROVIDERS:
        raise ProviderError(
            f"Proveedor '{provider}' no soportado. Usa uno de: {', '.join(SUPPORTED_PROVIDERS)}."
        )
    key = settings.api_key_for(provider)
    if not key:
        raise ProviderError(
            f"Falta la API key del proveedor seleccionado ('{provider}'). "
            f"Configura {provider.upper()}_API_KEY en tu archivo .env."
        )
    return key


# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------

def embed_texts(texts: list[str], provider: str | None = None) -> list[list[float]]:
    """Calcula embeddings para una lista de textos con el proveedor configurado."""
    provider = provider or settings.EMBEDDINGS_PROVIDER
    key = _require_key(provider)

    try:
        if provider == "openai":
            from openai import OpenAI

            client = OpenAI(api_key=key)
            response = client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL, input=texts
            )
            return [item.embedding for item in response.data]

        if provider == "gemini":
            import google.generativeai as genai

            genai.configure(api_key=key)
            result = genai.embed_content(
                model=settings.GEMINI_EMBEDDING_MODEL, content=texts
            )
            return result["embedding"]

        # cohere
        import cohere

        client = cohere.ClientV2(api_key=key)
        response = client.embed(
            texts=texts,
            model=settings.COHERE_EMBEDDING_MODEL,
            input_type="search_document",
            embedding_types=["float"],
        )
        return response.embeddings.float

    except ProviderError:
        raise
    except ImportError as exc:
        raise ProviderError(
            f"El SDK del proveedor '{provider}' no está instalado: {exc}. "
            "Revisa requirements.txt e instala las dependencias."
        ) from exc
    except Exception as exc:
        raise ProviderError(
            f"Error al generar embeddings con '{provider}': {exc}"
        ) from exc


def embed_query(text: str, provider: str | None = None) -> list[float]:
    """Embedding de una consulta de usuario (input_type de búsqueda en Cohere)."""
    provider = provider or settings.EMBEDDINGS_PROVIDER
    if provider == "cohere":
        key = _require_key(provider)
        try:
            import cohere

            client = cohere.ClientV2(api_key=key)
            response = client.embed(
                texts=[text],
                model=settings.COHERE_EMBEDDING_MODEL,
                input_type="search_query",
                embedding_types=["float"],
            )
            return response.embeddings.float[0]
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError(
                f"Error al generar el embedding de la consulta con 'cohere': {exc}"
            ) from exc
    return embed_texts([text], provider=provider)[0]


# ---------------------------------------------------------------------------
# Generación
# ---------------------------------------------------------------------------

def generate_text(prompt: str, provider: str | None = None) -> str:
    """Genera la respuesta del LLM con el proveedor configurado."""
    provider = provider or settings.MODEL_PROVIDER
    key = _require_key(provider)

    try:
        if provider == "openai":
            from openai import OpenAI

            client = OpenAI(api_key=key)
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()

        if provider == "gemini":
            import google.generativeai as genai

            genai.configure(api_key=key)
            model = genai.GenerativeModel(settings.GEMINI_MODEL)
            response = model.generate_content(prompt)
            return response.text.strip()

        # cohere
        import cohere

        client = cohere.ClientV2(api_key=key)
        response = client.chat(
            model=settings.COHERE_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.message.content[0].text.strip()

    except ProviderError:
        raise
    except ImportError as exc:
        raise ProviderError(
            f"El SDK del proveedor '{provider}' no está instalado: {exc}. "
            "Revisa requirements.txt e instala las dependencias."
        ) from exc
    except Exception as exc:
        raise ProviderError(
            f"Error al generar la respuesta con '{provider}': {exc}"
        ) from exc
