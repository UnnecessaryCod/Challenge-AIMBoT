"""
AIMBOT Knowledge Agent — interfaz Streamlit con branding AIMTALENT.
Flujo RAG: base documental limpia → ChromaDB → retrieval → LLM → respuesta con fuentes.
Las fuentes se muestran como enlaces de descarga directa del documento.
"""

import base64
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import settings
from src.config.providers import ProviderError
from src.generation.response_generator import generate_response
from src.ingestion.document_loader import load_markdown_documents
from src.retrieval.vector_store import build_vector_store, vector_store_exists

# --- Branding -----------------------------------------------------------------

BRAND_BLUE = "#2e4cff"
BRAND_BLUE_DEEP = "#0037c1"
BRAND_BLACK = "#030303"
BRAND_GRAY_BG = "#F7F8FC"
BRAND_GRAY_BORDER = "#E6E8F0"
BRAND_GRAY_TEXT = "#5F6472"

LOGO_PATH = PROJECT_ROOT / "assets" / "branding" / "logo_aimtalent_principal.png"
ISOTIPO_PATH = PROJECT_ROOT / "assets" / "branding" / "isotipo_aimtalent_azul.png"

WELCOME_MESSAGE = (
    "Hola, soy **AimBot de AIMTALENT**.\n\n"
    "Estoy aquí para ayudarte a identificar la solución más adecuada para tu reto de "
    "talento, liderazgo o gestión humana.\n\n"
    "Cuéntame brevemente qué necesitas resolver y te acompañaré con algunas preguntas "
    "para orientar mejor tu requerimiento."
)


def _b64(path: Path) -> str:
    """Codifica un archivo en base64 para incrustarlo en HTML (vacío si no existe)."""
    try:
        return base64.b64encode(path.read_bytes()).decode()
    except Exception:
        return ""


def source_download_link(filename: str) -> str:
    """
    Enlace de descarga directa del documento fuente.
    El nombre del archivo es el texto del enlace; al hacer clic se descarga.
    """
    path = Path(settings.DOCUMENTS_PATH) / filename
    encoded = _b64(path)
    if not encoded:
        return f'<span class="aim-source-chip aim-source-missing">📄 {filename}</span>'
    return (
        f'<a class="aim-source-chip" download="{filename}" '
        f'href="data:text/markdown;base64,{encoded}" '
        f'title="Descargar {filename}">📄 {filename}</a>'
    )


def render_sources(sources: list[dict]) -> None:
    """Muestra las fuentes como chips de descarga dentro de un expander."""
    if not sources:
        return
    with st.expander("📄 Fuentes utilizadas — clic para descargar"):
        chips = "".join(
            f'<div class="aim-source-row">{source_download_link(s["source"])}'
            f'<span class="aim-source-cat">{s["category"]}</span></div>'
            for s in sources
        )
        st.markdown(f'<div class="aim-sources">{chips}</div>', unsafe_allow_html=True)


st.set_page_config(
    page_title="AIMBOT Knowledge Agent",
    page_icon=str(ISOTIPO_PATH) if ISOTIPO_PATH.exists() else "🤖",
    layout="centered",
)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    h1, h2, h3,
    .aim-hero-title, .aim-hero-sub, .aim-badge,
    .aim-source-chip, .aim-source-cat, .aim-footer a,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatInput"] textarea {{
        font-family: 'Poppins', 'Segoe UI', sans-serif !important;
    }}
    .stApp {{
        background:
            radial-gradient(circle at 120% -10%, rgba(46, 76, 255, 0.07) 0%, transparent 45%),
            radial-gradient(circle at -20% 110%, rgba(46, 76, 255, 0.06) 0%, transparent 40%),
            {BRAND_GRAY_BG};
    }}
    h1, h2, h3 {{
        font-family: 'Poppins', sans-serif;
        color: {BRAND_BLACK};
        font-weight: 800;
        letter-spacing: -0.5px;
    }}

    /* --- Hero --- */
    .aim-hero {{
        display: flex;
        align-items: center;
        gap: 1.4rem;
        background: #FFFFFF;
        border: 1px solid {BRAND_GRAY_BORDER};
        border-radius: 18px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 24px rgba(3, 55, 193, 0.07);
        border-top: 5px solid {BRAND_BLUE};
    }}
    .aim-hero img {{
        width: 110px;
        flex-shrink: 0;
    }}
    .aim-hero-title {{
        font-size: 1.75rem;
        font-weight: 800;
        color: {BRAND_BLACK};
        letter-spacing: -0.5px;
        line-height: 1.15;
    }}
    .aim-hero-sub {{
        color: {BRAND_GRAY_TEXT};
        font-size: 0.98rem;
        font-weight: 500;
        margin-top: 0.15rem;
    }}
    .aim-badges {{
        margin-top: 0.65rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
    }}
    .aim-badge {{
        background: rgba(46, 76, 255, 0.08);
        color: {BRAND_BLUE_DEEP};
        border: 1px solid rgba(46, 76, 255, 0.25);
        border-radius: 999px;
        padding: 0.14rem 0.7rem;
        font-size: 0.72rem;
        font-weight: 600;
    }}

    /* --- Chat --- */
    [data-testid="stChatMessage"] {{
        background-color: #FFFFFF;
        border: 1px solid {BRAND_GRAY_BORDER};
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        box-shadow: 0 2px 10px rgba(3, 55, 193, 0.04);
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        background-color: #EEF1FF;
        border-color: rgba(46, 76, 255, 0.30);
    }}
    [data-testid="stChatInput"] {{
        border-radius: 14px;
    }}
    [data-testid="stChatInput"] textarea {{
        font-family: 'Poppins', sans-serif;
    }}

    /* --- Fuentes descargables --- */
    .aim-sources {{
        display: flex;
        flex-direction: column;
        gap: 0.45rem;
    }}
    .aim-source-row {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        flex-wrap: wrap;
    }}
    .aim-source-chip {{
        display: inline-block;
        background: #FFFFFF;
        color: {BRAND_BLUE} !important;
        border: 1.5px solid {BRAND_BLUE};
        border-radius: 999px;
        padding: 0.22rem 0.85rem;
        font-size: 0.82rem;
        font-weight: 600;
        text-decoration: none !important;
        transition: all 0.15s ease-in-out;
    }}
    .aim-source-chip:hover {{
        background: {BRAND_BLUE};
        color: #FFFFFF !important;
        box-shadow: 0 3px 10px rgba(46, 76, 255, 0.35);
    }}
    .aim-source-missing {{
        border-color: {BRAND_GRAY_BORDER};
        color: {BRAND_GRAY_TEXT} !important;
    }}
    .aim-source-cat {{
        color: {BRAND_GRAY_TEXT};
        font-size: 0.78rem;
        font-weight: 500;
    }}

    /* --- Botones --- */
    .stButton > button {{
        background: linear-gradient(135deg, {BRAND_BLUE} 0%, {BRAND_BLUE_DEEP} 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        padding: 0.55rem 1.2rem;
        transition: all 0.15s ease-in-out;
    }}
    .stButton > button:hover {{
        box-shadow: 0 4px 14px rgba(46, 76, 255, 0.40);
        color: #FFFFFF;
        transform: translateY(-1px);
    }}

    /* --- Sidebar --- */
    [data-testid="stSidebar"] {{
        background-color: #FFFFFF;
        border-right: 1px solid {BRAND_GRAY_BORDER};
    }}
    [data-testid="stSidebar"] .stMarkdown h3 {{
        color: {BRAND_BLUE_DEEP};
        font-size: 1.02rem;
    }}

    /* --- Footer --- */
    .aim-footer {{
        background: linear-gradient(135deg, {BRAND_BLUE} 0%, {BRAND_BLUE_DEEP} 100%);
        border-radius: 14px;
        text-align: center;
        padding: 0.9rem 1rem;
        margin-top: 2.2rem;
        box-shadow: 0 4px 18px rgba(3, 55, 193, 0.25);
    }}
    .aim-footer a {{
        color: #FFFFFF !important;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0 0.8rem;
    }}
    .aim-footer a:hover {{
        text-decoration: underline;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header (hero con logo) -----------------------------------------------------

logo_b64 = _b64(LOGO_PATH)
logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="AIMTALENT">' if logo_b64 else ""

st.markdown(
    f"""
    <div class="aim-hero">
        {logo_html}
        <div>
            <div class="aim-hero-title">AIMBOT Knowledge Agent</div>
            <div class="aim-hero-sub">Agente comercial consultivo de AIMTALENT</div>
            <div class="aim-badges">
                <span class="aim-badge">Executive Search</span>
                <span class="aim-badge">Hiring Solutions</span>
                <span class="aim-badge">Consulting</span>
                <span class="aim-badge">Advisory</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---------------------------------------------------------------------

with st.sidebar:
    if ISOTIPO_PATH.exists():
        st.image(str(ISOTIPO_PATH), width=56)
    st.markdown("### Estado del sistema")

    api_key_ok = bool(settings.api_key_for(settings.MODEL_PROVIDER))
    docs_count = len(load_markdown_documents())
    index_ok = vector_store_exists()

    st.markdown(
        f"""
- Proveedor LLM: `{settings.MODEL_PROVIDER}`
- Embeddings: `{settings.EMBEDDINGS_PROVIDER}`
- API key: {"✅ configurada" if api_key_ok else "⚠️ falta configurar"}
- Documentos limpios: **{docs_count}**
- Índice vectorial: {"✅ listo" if index_ok else "⚠️ pendiente"}
"""
    )

    if st.button("🔄 Reconstruir base vectorial", use_container_width=True):
        try:
            with st.spinner("Reconstruyendo índice vectorial..."):
                total = build_vector_store(rebuild=True)
            st.success(f"Índice reconstruido con {total} fragmentos.")
            st.rerun()
        except ProviderError as exc:
            st.error(str(exc))
        except Exception:
            st.error("No fue posible reconstruir el índice. Revisa la configuración del .env.")

    st.markdown("---")
    st.markdown("### Alcance V1")
    st.caption(
        "AimBot responde sobre AIMTALENT: Executive Search, Hiring Solutions, "
        "Consulting, Advisory, metodología AimTarget, trazabilidad y diagnóstico "
        "comercial. Usa únicamente la base documental limpia, sin datos de clientes "
        "ni información sensible."
    )

# --- Conversación -----------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE, "sources": []}
    ]

for message in st.session_state.messages:
    avatar = str(ISOTIPO_PATH) if (message["role"] == "assistant" and ISOTIPO_PATH.exists()) else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        render_sources(message.get("sources", []))

user_question = st.chat_input("Escribe tu pregunta o cuéntame tu reto...")

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question, "sources": []})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant", avatar=str(ISOTIPO_PATH) if ISOTIPO_PATH.exists() else None):
        if not settings.api_key_for(settings.MODEL_PROVIDER):
            answer = (
                f"⚠️ Falta la API key del proveedor seleccionado (`{settings.MODEL_PROVIDER}`). "
                f"Configura `{settings.MODEL_PROVIDER.upper()}_API_KEY` en tu archivo `.env` "
                "para que pueda responder con la base documental."
            )
            st.warning(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer, "sources": []})
        else:
            try:
                if not vector_store_exists():
                    with st.spinner("Preparando la base vectorial por primera vez..."):
                        build_vector_store()
                with st.spinner("Consultando la base documental de AIMTALENT..."):
                    result = generate_response(user_question)
                st.markdown(result["answer"])
                render_sources(result["sources"])
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"],
                    }
                )
            except ProviderError as exc:
                st.error(str(exc))
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"⚠️ {exc}", "sources": []}
                )
            except Exception:
                friendly = (
                    "Ocurrió un error inesperado al procesar tu consulta. "
                    "Verifica tu conexión y la configuración del archivo `.env`, e inténtalo nuevamente."
                )
                st.error(friendly)
                st.session_state.messages.append(
                    {"role": "assistant", "content": friendly, "sources": []}
                )

# --- Footer ------------------------------------------------------------------------

st.markdown(
    """
    <div class="aim-footer">
        <a href="https://www.aimtalent.com" target="_blank">🌐 www.aimtalent.com</a>
        <a href="https://www.instagram.com/aimtalent.global" target="_blank">📷 @aimtalent.global</a>
    </div>
    """,
    unsafe_allow_html=True,
)
