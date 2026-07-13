# Challenge AIMTALENT — AIMBOT Knowledge Agent

## VIDEO PRESENTACIÓN: https://drive.google.com/file/d/1oDanlrO4C8zOiX9H8ymXtJ1A91uptLHh/view?usp=sharing

## 1. Descripción del proyecto

**AIMBOT Knowledge Agent** es un agente de inteligencia artificial comercial y consultivo de AIMTALENT. Responde preguntas sobre servicios, unidades de negocio, metodología AimTarget, trazabilidad y levantamiento de requerimientos comerciales, usando exclusivamente una **base documental limpia y anonimizada**.

La aplicación funciona bajo lógica **RAG (Retrieval-Augmented Generation)**: recupera los fragmentos documentales más relevantes para cada pregunta y genera una respuesta fundamentada, mostrando siempre las fuentes utilizadas.

## Demo desplegada en Oracle Cloud Infrastructure

La aplicación AIMBOT Knowledge Agent fue desplegada en Oracle Cloud Infrastructure utilizando una instancia Compute con Ubuntu, Python y Streamlit.

**URL pública de la demo:** http://148.116.110.214:8501

**Stack del despliegue:**

- Oracle Cloud Infrastructure Compute Instance
- Ubuntu 22.04
- Python 3.10
- Streamlit
- ChromaDB
- Gemini API
- GitHub

## 2. Objetivo

- Responder preguntas sobre AIMTALENT y sus unidades de negocio.
- Orientar al usuario hacia la solución adecuada (Executive Search, Hiring Solutions, Consulting, Advisory).
- Guiar el diagnóstico comercial con preguntas útiles.
- Recopilar información clave para preparar una propuesta.
- Evitar respuestas inventadas y mostrar fuentes documentales.
- Funcionar localmente y quedar lista para deploy en Oracle Cloud Infrastructure (OCI).

## 3. Alcance V1 (MVP)

**Incluye:** institucional AIMTALENT, Executive Search, Hiring Solutions, Consulting, Advisory, metodología AimTarget, trazabilidad y plataforma, checklist de diagnóstico comercial.

**No incluye:** nombres de clientes, políticas internas, correos o teléfonos personales, honorarios específicos, CRM, integraciones con WhatsApp/Slack/correo, autenticación avanzada ni cotizador automático.

## 4. Arquitectura RAG

```text
Documentos limpios AIMTALENT (data/raw/*.md)
        ↓
Carga documental con metadata (fuente + categoría)
        ↓
Chunking (~1000 caracteres, overlap 150, sección conservada)
        ↓
Embeddings (OpenAI / Gemini / Cohere)
        ↓
Base vectorial ChromaDB (data/processed/vector_store)
        ↓
Pregunta del usuario en Streamlit
        ↓
Retrieval semántico (Top K = 5, filtro de relevancia)
        ↓
LLM con prompt de AimBot
        ↓
Respuesta con fuentes (o fallback si no hay evidencia)
```

## 5. Estructura del repositorio

```text
challenge_aimtalent/
│
├── app/
│   └── streamlit_app.py          # Interfaz Streamlit con branding AIMTALENT
│
├── data/
│   ├── raw/                      # Base documental limpia (Markdown)
│   └── processed/
│       └── vector_store/         # Índice ChromaDB (no se versiona)
│
├── docs/
│   ├── base_conocimiento.md
│   ├── matriz_documental.md
│   ├── arquitectura.md
│   └── deploy_oci.md             # Guía de despliegue en OCI
│
├── src/
│   ├── ingestion/document_loader.py    # Carga Markdown + chunking con metadata
│   ├── retrieval/vector_store.py       # ChromaDB: crear, persistir, reconstruir, buscar
│   ├── generation/response_generator.py # Respuesta con fuentes y fallback
│   ├── prompts/aimbot_prompt.py        # Prompt base de AimBot
│   └── config/
│       ├── settings.py                 # Variables de entorno
│       └── providers.py                # OpenAI / Gemini / Cohere
│
├── assets/
│   ├── branding/                 # Logo, isotipo y referencia de marca
│   ├── screenshots/              # Evidencia de funcionamiento
│   └── demo/                     # Video demo
│
├── tests/
│   └── test_basic_flow.py        # Pruebas básicas (sin llamadas a APIs)
│
├── requirements.txt
├── .env.example
├── .gitignore
├── CLAUDE.md
└── README.md
```

## 6. Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Interfaz | Streamlit |
| Base vectorial | ChromaDB (persistente, local) |
| Embeddings y LLM | OpenAI / Google Gemini / Cohere (seleccionable por `.env`) |
| Configuración | python-dotenv |
| Pruebas | pytest |
| Deploy | Oracle Cloud Infrastructure (Compute Instance) |

> **Decisión técnica:** no se usa LangChain. El flujo RAG se implementa directamente con ChromaDB y los SDK oficiales de cada proveedor, lo que reduce dependencias y mantiene el código simple y trazable.

## 7. Branding aplicado

La interfaz respeta la identidad visual de AIMTALENT:

- Azul principal `#2e4cff`, azul profundo `#0037c1`, negro `#030303`, gris fondo `#F7F8FC`, gris borde `#E6E8F0`.
- Logo principal en el header e isotipo "A" como avatar de AimBot y en el sidebar.
- Cards blancas para la conversación, botones en azul AIMTALENT.
- Sidebar con estado del sistema, botón de reconstrucción del índice y alcance V1.
- Footer con `www.aimtalent.com` y `@aimtalent.global`.
- Si los logos no existen, la app sigue funcionando sin romperse.

## 8. Instalación local

```bash
git clone https://github.com/usuario/challenge-aimtalent.git
cd challenge_aimtalent
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / Mac
pip install -r requirements.txt
```

## 9. Variables de entorno

Copiar `.env.example` a `.env` y completar la API key del proveedor elegido:

```bash
cp .env.example .env
```

```env
MODEL_PROVIDER=openai          # openai | gemini | cohere
EMBEDDINGS_PROVIDER=openai

OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

GEMINI_API_KEY=...
COHERE_API_KEY=...

VECTOR_DB_PATH=data/processed/vector_store
DOCUMENTS_PATH=data/raw
TOP_K=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
```

Reglas: no hardcodear API keys, no subir `.env` al repositorio (ya está en `.gitignore`). Si falta la API key del proveedor seleccionado, la app muestra un mensaje claro en lugar de romperse.

## 10. Cómo ejecutar la aplicación

```bash
streamlit run app/streamlit_app.py
```

La app abre en `http://localhost:8501`. En la primera pregunta, si el índice vectorial no existe, se construye automáticamente.

## 11. Cómo reconstruir la base vectorial

Desde la interfaz: botón **"🔄 Reconstruir base vectorial"** en el sidebar.

Desde consola:

```bash
python -c "import sys; sys.path.insert(0,'.'); from src.retrieval.vector_store import build_vector_store; print(build_vector_store(rebuild=True), 'fragmentos indexados')"
```

## 12. Ejemplos de preguntas

1. ¿Qué servicios ofrece AIMTALENT?
2. ¿Cuál es la diferencia entre Executive Search y Hiring Solutions?
3. ¿Qué información necesitan para iniciar una búsqueda ejecutiva?
4. ¿Cómo funciona la metodología AimTarget?
5. ¿Qué preguntas debo responder para solicitar un programa de liderazgo?
6. ¿Qué incluye un proceso de evaluación psicolaboral?
7. ¿AIMTALENT puede operar en LATAM?
8. ¿Qué datos necesita el equipo para preparar una propuesta?
9. Necesito contratar 20 operarios, ¿qué servicio me recomiendas?
10. Necesito desarrollar líderes, ¿qué solución podría aplicar?

## 13. Ejemplos de respuestas

**Pregunta:** ¿Qué información necesitan para iniciar una búsqueda ejecutiva?

**Respuesta esperada:** Para iniciar una búsqueda ejecutiva, AIMTALENT necesita conocer la posición requerida, nomenclatura del cargo, banda salarial, país o ciudad, fecha esperada de inicio y perfil del puesto. Si el perfil aún no está definido, puede co-crearse en una sesión de calibración bajo la metodología AimTarget. *(Con sección de fuentes: `03_executive_search.md`.)*

**Pregunta fuera de alcance:** ¿Cuál es la política de vacaciones de AIMTALENT?

**Respuesta esperada:**

```text
No encontré información suficiente en la base documental disponible para responder con precisión.
```

## 14. Reglas de seguridad documental

El agente usa **únicamente** la base documental limpia (`data/raw`). Los documentos internos de configuración y control (`00_readme_base_conocimiento.md`, `02_aimbot_comportamiento.md`, `09_matriz_documental_limpia.md`) **no se indexan en el vector store ni aparecen como fuentes visibles**; solo se muestran documentos comerciales, metodológicos e institucionales aptos para usuario final. Además, no incluye ni debe reintroducirse:

- Nombres de clientes reales ni logos de clientes.
- Políticas internas.
- Correos o teléfonos personales.
- RUC ni datos tributarios.
- Honorarios específicos por cliente.
- Información confidencial de propuestas reales o comentarios internos.

Si una pregunta no tiene respaldo documental, AimBot responde con el mensaje de fallback en lugar de inventar.

## 15. Deploy en Oracle Cloud Infrastructure

Guía completa en [docs/deploy_oci.md](docs/deploy_oci.md). Resumen: crear una OCI Compute Instance, clonar el repo, instalar dependencias, configurar `.env`, abrir el puerto 8501 y ejecutar:

```bash
streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 16. Evidencia de funcionamiento

- **Demo pública en OCI:** http://148.116.110.214:8501
- Capturas de la app funcionando: `assets/screenshots/`
- Video demo: `assets/demo/`

Capturas del despliegue en OCI (`assets/screenshots/`):

| Captura | Contenido |
|---|---|
| [01_home_oci.png](assets/screenshots/01_home_oci.png) | Pantalla inicial de AimBot en la URL pública de OCI, con avatar y preguntas sugeridas |
| [02_hiring_response.png](assets/screenshots/02_hiring_response.png) | Respuesta consultiva sobre Hiring Solutions con preguntas de diagnóstico |
| [03_sources_reference.png](assets/screenshots/03_sources_reference.png) | Expander "Fuentes de referencia" con documentos comerciales descargables |
| [04_fallback_out_of_scope.png](assets/screenshots/04_fallback_out_of_scope.png) | Pregunta fuera de alcance con fallback orientador, sin fuentes |
| [05_oci_instance_running.png](assets/screenshots/05_oci_instance_running.png) | Instancia Compute de OCI en estado Running |
| [06_terminal_streamlit_running.png](assets/screenshots/06_terminal_streamlit_running.png) | Actualización del repo y Streamlit corriendo en la instancia (tmux + curl 200) |

## 17. Pruebas

```bash
python -m pytest tests -q
```

Cubren carga documental, inferencia de categoría, chunking, prompt de AimBot y mensaje de fallback, sin llamadas a APIs externas.

## 18. Próximos pasos

1. Capturar evidencia visual local (screenshots y video demo).
2. Ejecutar el deploy en OCI y registrar evidencia.
3. Validar las 12 preguntas obligatorias con la API key configurada.
4. Iterar la base documental limpia según feedback comercial.
