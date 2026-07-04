"""
Configuración central del proyecto AIMBOT Knowledge Agent.
Lee variables desde .env y expone valores con defaults seguros.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _resolve(path_str: str) -> str:
    """Convierte rutas relativas del .env en rutas absolutas al root del proyecto."""
    path = Path(path_str)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return str(path)


# Proveedores activos
MODEL_PROVIDER = _env("MODEL_PROVIDER", "openai").lower()
EMBEDDINGS_PROVIDER = _env("EMBEDDINGS_PROVIDER", MODEL_PROVIDER).lower()

# OpenAI
OPENAI_API_KEY = _env("OPENAI_API_KEY")
OPENAI_MODEL = _env("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = _env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# Gemini
GEMINI_API_KEY = _env("GEMINI_API_KEY")
GEMINI_MODEL = _env("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_EMBEDDING_MODEL = _env("GEMINI_EMBEDDING_MODEL", "models/text-embedding-004")

# Cohere
COHERE_API_KEY = _env("COHERE_API_KEY")
COHERE_MODEL = _env("COHERE_MODEL", "command-r-plus")
COHERE_EMBEDDING_MODEL = _env("COHERE_EMBEDDING_MODEL", "embed-multilingual-v3.0")

# RAG
VECTOR_DB_PATH = _resolve(_env("VECTOR_DB_PATH", "data/processed/vector_store"))
DOCUMENTS_PATH = _resolve(_env("DOCUMENTS_PATH", "data/raw"))
TOP_K = int(_env("TOP_K", "5"))
CHUNK_SIZE = int(_env("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(_env("CHUNK_OVERLAP", "150"))

# Distancia coseno máxima para considerar un fragmento relevante.
# Por encima de este valor el fragmento se descarta y puede activarse el fallback.
MAX_DISTANCE = float(_env("MAX_DISTANCE", "0.75"))

COLLECTION_NAME = "aimtalent_base_limpia"

# Placeholders del .env.example que no deben tratarse como credenciales reales
_PLACEHOLDER_PREFIXES = ("your_", "colocar", "tu_")


def api_key_for(provider: str) -> str:
    """Devuelve la API key del proveedor, o cadena vacía si no está configurada."""
    key = {
        "openai": OPENAI_API_KEY,
        "gemini": GEMINI_API_KEY,
        "cohere": COHERE_API_KEY,
    }.get(provider, "")
    if key.lower().startswith(_PLACEHOLDER_PREFIXES):
        return ""
    return key
