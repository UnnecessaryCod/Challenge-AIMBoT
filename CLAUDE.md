# CLAUDE.md — Challenge AIMTALENT / AIMBOT Knowledge Agent

## 1. Rol que debes asumir

Actúa como un **Senior AI Engineer, Python Developer, arquitecto RAG y UI developer especializado en Streamlit**.

Tu misión es revisar, refinar, completar y dejar funcional el proyecto:

# Challenge AIMTALENT — AIMBOT Knowledge Agent

El proyecto busca construir un agente de inteligencia artificial comercial y consultivo para AIMTALENT, capaz de responder preguntas sobre servicios, unidades de negocio, metodología, trazabilidad y levantamiento de requerimientos comerciales a partir de una base documental limpia y anonimizada.

El agente debe usar lógica **RAG**:

```text
Documentos limpios → Chunks → Embeddings → Vector Store → Retrieval → LLM → Respuesta con fuentes
```

Además, la aplicación debe verse como una solución oficial de AIMTALENT, respetando colores, logos, tono ejecutivo y presentación profesional.

---

## 2. Contexto del proyecto

AIMTALENT necesita un agente comercial consultivo, llamado **AimBot**, que permita orientar a potenciales clientes o usuarios internos comerciales sobre:

- Qué servicios ofrece AIMTALENT.
- Qué unidad de negocio corresponde a una necesidad específica.
- Qué información se necesita para preparar una propuesta.
- Qué preguntas debe responder un cliente para diagnosticar mejor su reto.
- Cómo funcionan las metodologías, procesos y entregables principales.
- Cómo diferenciar Executive Search, Hiring Solutions, Consulting y Advisory.

La solución debe ser un MVP sólido, funcional, demostrable y preparado para deploy en **Oracle Cloud Infrastructure (OCI)**.

---

## 3. Objetivo general

Construir una aplicación funcional con Streamlit que permita conversar con AimBot usando una base documental limpia de AIMTALENT.

AimBot debe:

1. Responder preguntas sobre AIMTALENT.
2. Explicar servicios de Executive Search, Hiring Solutions, Consulting y Advisory.
3. Guiar al usuario con preguntas de diagnóstico comercial.
4. Recoger información clave para preparar una propuesta.
5. Responder con tono ejecutivo, cálido, consultivo y comercial.
6. Evitar respuestas inventadas.
7. Mostrar las fuentes documentales utilizadas.
8. Funcionar localmente.
9. Quedar preparada para despliegue en Oracle Cloud Infrastructure.
10. Verse visualmente alineado a la marca AIMTALENT.

---

## 4. Insumos disponibles

El proyecto cuenta con estos insumos:

### 4.1. Repositorio base

Archivo:

```text
challenge_aimtalent_repo_base.zip
```

Contiene:

- Estructura inicial del repositorio.
- README técnico inicial.
- App base en Streamlit.
- Carpetas para código, documentos, tests y assets.
- Placeholders de módulos para ingesta, recuperación y generación.

### 4.2. Base de conocimiento limpia

Archivo:

```text
aimbot_base_conocimiento_limpia_v1.zip
```

Contiene documentos Markdown limpios, anonimizados y preparados para RAG.

No contiene:

- Nombres de clientes reales.
- Políticas internas.
- Correos personales.
- Honorarios específicos.
- Información sensible.

### 4.3. Matriz documental

Archivo:

```text
matriz_documental_aimbot_limpia_v1.xlsx
```

Contiene:

- Clasificación documental.
- Categoría de cada archivo.
- Uso previsto.
- Estado.
- Acción requerida.

### 4.4. Assets visuales de marca

Se cuenta con referencias visuales de AIMTALENT:

- Logo principal AIMTALENT.
- Isotipo “A”.
- Referencia de colores y estilo visual.
- Paleta de marca.

Estos assets deben incorporarse en la app Streamlit en una carpeta:

```text
assets/branding/
```

---

## 5. Restricciones críticas de seguridad documental

No debes incluir ni reintroducir:

- Nombres de clientes reales.
- Políticas internas de AIMTALENT.
- Correos personales.
- Teléfonos personales.
- RUC.
- Honorarios específicos por cliente.
- Logos de clientes.
- Información confidencial de propuestas reales.
- Comentarios internos de trabajo.
- Información no respaldada por documentos.
- Información que no exista en la base documental limpia.

Si encuentras información sensible en algún archivo, debes excluirla o advertirlo antes de usarla.

---

## 6. Alcance de la versión V1

Esta primera versión será un **MVP / POC comercial**.

### 6.1. Incluye

- Información institucional de AIMTALENT.
- Propuesta de valor.
- Cobertura geográfica.
- Executive Search.
- Hiring Solutions.
- Consulting.
- Advisory.
- Metodología AimTarget.
- Trazabilidad del servicio.
- Plataforma y dashboards.
- Checklist de diagnóstico comercial.
- Preguntas clave para levantar información de propuesta.

### 6.2. No incluye

- Políticas internas.
- Bot de recursos humanos interno.
- Gestión de vacaciones, cumpleaños o beneficios.
- CRM.
- Integración con WhatsApp.
- Integración con correo.
- Integración con Slack o Teams.
- Autenticación avanzada.
- Base de datos de clientes.
- Cotizador automático.
- Deploy productivo definitivo.

---

## 7. Stack técnico recomendado

Usa una arquitectura simple, funcional y mantenible.

### 7.1. Tecnologías principales

- Python.
- Streamlit.
- ChromaDB.
- LangChain, solo si aporta orden.
- OpenAI o proveedor compatible para embeddings y generación.
- python-dotenv.
- Markdown como base documental inicial.

### 7.2. Tecnologías opcionales

- Pandas para lectura de matriz documental.
- PyPDF si se decide incorporar PDF más adelante.
- tiktoken para control de tokens.
- pytest para pruebas básicas.

---

## 8. Estructura esperada del repositorio

Mantén o mejora esta estructura:

```text
challenge_aimtalent/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   └── processed/
│       └── vector_store/
│
├── docs/
│   ├── base_conocimiento.md
│   ├── matriz_documental.md
│   ├── arquitectura.md
│   └── deploy_oci.md
│
├── src/
│   ├── ingestion/
│   │   └── document_loader.py
│   ├── retrieval/
│   │   └── vector_store.py
│   ├── generation/
│   │   └── response_generator.py
│   ├── prompts/
│   │   └── aimbot_prompt.py
│   └── config/
│       └── settings.py
│
├── tests/
│   └── test_basic_flow.py
│
├── assets/
│   ├── branding/
│   │   ├── logo_aimtalent.png
│   │   ├── isotipo_aimtalent.png
│   │   └── paleta_aimtalent.png
│   ├── screenshots/
│   └── demo/
│
├── requirements.txt
├── .env.example
├── .gitignore
├── CLAUDE.md
└── README.md
```

Puedes hacer ajustes si mejoran claridad y mantenibilidad, pero no compliques innecesariamente el proyecto.

---

## 9. Branding e identidad visual de AIMTALENT

La aplicación debe respetar la identidad visual de AIMTALENT.

### 9.1. Objetivo visual

La app debe verse:

- Ejecutiva.
- Limpia.
- Moderna.
- Profesional.
- Tecnológica.
- Coherente con la marca AIMTALENT.
- Minimalista, pero con presencia visual.
- Lista para una demo corporativa.

No debe verse como un prototipo genérico de Streamlit.

### 9.2. Colores de marca

Usa prioritariamente estos colores:

```text
Azul principal: #2e4cff
Azul profundo:  #0037c1
Negro texto:    #030303
Blanco:         #FFFFFF
```

Puedes usar grises suaves para fondos, bordes y divisores:

```text
Gris fondo:     #F7F8FC
Gris borde:     #E6E8F0
Gris texto:     #5F6472
```

### 9.3. Uso de logos

Incorpora los logos oficiales de AIMTALENT:

- Logo principal AIMTALENT.
- Isotipo “A”.
- Referencia visual de paleta.

Reglas:

1. Mostrar el logo principal en el header o sidebar.
2. Usar el isotipo como refuerzo visual si aporta al diseño.
3. No deformar los logos.
4. No saturar la interfaz con elementos gráficos.
5. Si los archivos no existen, la app debe seguir funcionando sin romperse.
6. Crear la carpeta `assets/branding/` si no existe.

### 9.4. UI recomendada en Streamlit

La app debe incluir:

- Header superior con logo AIMTALENT.
- Título: `AIMBOT Knowledge Agent`.
- Subtítulo: `Agente comercial consultivo de AIMTALENT`.
- Mensaje de bienvenida.
- Input conversacional.
- Botón principal con azul AIMTALENT.
- Respuesta en card blanca.
- Fuentes utilizadas en bloque desplegable o caja secundaria.
- Sidebar con branding, estado del sistema, botón para reconstruir índice vectorial e información de alcance.
- Footer con `www.aimtalent.com` y `@aimtalent.global`.

### 9.5. CSS en Streamlit

Implementa CSS embebido usando:

```python
st.markdown(
    """
    <style>
    ...
    </style>
    """,
    unsafe_allow_html=True
)
```

Debe personalizar:

- Botones.
- Títulos.
- Contenedores.
- Sidebar.
- Cards.
- Tipografía visual.
- Espaciado.
- Color de acento.

Mantén buena legibilidad y contraste.

---

## 10. Tono conversacional de AimBot

AimBot debe sonar:

- Ejecutivo.
- Claro.
- Cálido.
- Consultivo.
- Comercial.
- Seguro.
- Ordenado.
- Persuasivo sin ser invasivo.
- Orientado a solución.

AimBot no debe sonar:

- Robótico.
- Agresivo.
- Genérico.
- Excesivamente técnico.
- Desesperado por vender.
- Como si inventara información.
- Como formulario rígido.

---

## 11. Mensaje de bienvenida sugerido

Usa este mensaje o una versión mejorada:

```text
Hola, soy AimBot de AIMTALENT.
Estoy aquí para ayudarte a identificar la solución más adecuada para tu reto de talento, liderazgo o gestión humana.

Cuéntame brevemente qué necesitas resolver y te acompañaré con algunas preguntas para orientar mejor tu requerimiento.
```

---

## 12. Reglas funcionales de AimBot

AimBot debe:

1. Responder solo con base en la documentación cargada.
2. No inventar información.
3. Informar cuando no encuentre información suficiente.
4. Mantener tono ejecutivo y consultivo.
5. Mostrar fuentes utilizadas.
6. Guiar al usuario hacia la unidad de negocio adecuada.
7. Hacer preguntas de diagnóstico cuando corresponda.
8. Pedir correo corporativo cuando el usuario quiera avanzar con propuesta.
9. No mencionar clientes reales.
10. No revelar información sensible.
11. No responder sobre políticas internas excluidas.
12. No improvisar precios ni honorarios.

---

## 13. Prompt base de AimBot

Implementa un prompt similar a este en `src/prompts/aimbot_prompt.py`:

```text
Eres AimBot, agente comercial consultivo de AIMTALENT.

Tu objetivo es ayudar al usuario a identificar la solución más adecuada en talento, liderazgo o gestión humana, usando únicamente la información contenida en el contexto documental proporcionado.

Reglas obligatorias:
- Responde solo con base en el contexto.
- No inventes información.
- Si no encuentras información suficiente, indica: "No encontré información suficiente en la base documental disponible para responder con precisión."
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

Respuesta:
```

---

## 14. Datos comerciales que AimBot debe intentar recopilar

Cuando el usuario quiera avanzar o tenga una necesidad comercial, AimBot debe intentar recopilar de forma conversacional:

- Nombre completo.
- Cargo.
- Empresa.
- Sector.
- País o ciudad.
- Correo corporativo.
- Teléfono o WhatsApp.
- Cómo llegó a AIMTALENT.
- Servicio de interés.
- Urgencia o fecha estimada de inicio.
- Objetivo del proyecto.
- Dolor o necesidad principal.
- Volumen de posiciones o personas involucradas.
- Nivel de cargos involucrados.
- Si cuenta con perfil, brief o información previa.
- Si requiere cobertura en Perú, LATAM, España o USA.

No debe pedir todo de golpe si la conversación no lo amerita. Debe guiar con naturalidad.

---

## 15. Tareas principales de implementación

### 15.1. Revisar estructura actual

Antes de modificar, revisa:

- README.md
- requirements.txt
- app/streamlit_app.py
- src/ingestion/document_loader.py
- src/retrieval/vector_store.py
- src/generation/response_generator.py
- src/config/settings.py
- data/raw/
- docs/
- assets/

Luego propón brevemente mejoras y ejecútalas.

### 15.2. Integrar base documental limpia

Copia los archivos Markdown de la base limpia en:

```text
data/raw/
```

Debe quedar una base documental con archivos similares a:

```text
01_institucional_aimtalent.md
02_aimbot_comportamiento.md
03_executive_search.md
04_hiring_solutions.md
05_consulting.md
06_advisory.md
07_metodologia_y_trazabilidad.md
08_checklist_diagnostico_propuesta.md
```

No uses documentos crudos sensibles.

### 15.3. Implementar carga documental

Implementa una función para leer archivos `.md` desde `data/raw`.

Cada documento debe convertirse en una estructura con:

```python
{
    "content": "...",
    "metadata": {
        "source": "03_executive_search.md",
        "category": "Executive Search"
    }
}
```

Si la categoría no está explícita, infiérela desde el nombre del archivo.

### 15.4. Implementar chunking

Divide los documentos en fragmentos.

Recomendación:

```text
Chunk size: 800 a 1200 caracteres
Overlap: 100 a 200 caracteres
Top K retrieval: 4 o 5 fragmentos
```

Cada chunk debe conservar:

- Texto.
- Archivo fuente.
- Categoría.
- Número de chunk.
- Sección si es posible.

### 15.5. Implementar embeddings y ChromaDB

Crea una base vectorial local usando ChromaDB.

Debe existir una función para:

1. Crear índice vectorial.
2. Persistirlo en `data/processed/vector_store`.
3. Reutilizarlo si ya existe.
4. Reconstruirlo si el usuario lo solicita desde Streamlit.

Variables en `.env`:

```env
OPENAI_API_KEY=
VECTOR_DB_PATH=data/processed/vector_store
DOCUMENTS_PATH=data/raw
```

Si decides usar otro proveedor compatible, actualiza `.env.example` y README.

### 15.6. Implementar recuperación semántica

Crea una función que reciba una pregunta y devuelva los fragmentos más relevantes.

Requisitos:

- Top K: 4 o 5.
- Devolver texto + metadata.
- Mostrar fuentes en interfaz.
- Activar fallback si no hay contexto suficiente.
- Evitar respuestas cuando la pregunta esté fuera del alcance.

### 15.7. Implementar generación de respuesta

Crea una función que reciba:

- Pregunta del usuario.
- Contexto recuperado.
- Metadata de fuentes.

Debe devolver:

- Respuesta final.
- Fuentes utilizadas.
- Mensaje de fallback si no hay evidencia suficiente.

### 15.8. Mejorar interfaz Streamlit

La interfaz debe ser simple, limpia, ejecutiva y demostrable.

Debe incluir:

- Título: `AIMBOT Knowledge Agent`.
- Subtítulo: `Agente comercial consultivo de AIMTALENT`.
- Logo AIMTALENT.
- Mensaje de bienvenida.
- Caja de texto para consulta.
- Botón para enviar.
- Respuesta del agente.
- Fuentes utilizadas.
- Opción para reconstruir base vectorial.
- Mensaje claro si no hay API key configurada.
- Manejo básico de errores.
- Footer con web y red social.
- Estilo visual personalizado con colores de marca.

---

## 16. Modo diagnóstico comercial

Cuando el usuario no haga una pregunta específica, AimBot debe guiar el levantamiento de información.

Ejemplo de comportamiento:

```text
Para orientarte mejor, cuéntame:
1. ¿Qué reto necesitas resolver?
2. ¿Es una necesidad de selección, liderazgo, cultura, evaluación o desarrollo?
3. ¿Cuántas personas o posiciones están involucradas?
4. ¿En qué país o ciudad se ejecutaría?
5. ¿Para cuándo necesitas iniciar?
```

Debe adaptar sus preguntas según la unidad de negocio.

### Executive Search

Preguntar:

- ¿Qué posición buscas?
- ¿Cuál es la nomenclatura del cargo?
- ¿Cuál es la banda salarial aproximada?
- ¿Tienes el perfil del puesto?
- ¿Para cuándo deseas iniciar la búsqueda?
- ¿La búsqueda es en Perú, LATAM, España o USA?

### Hiring Solutions

Preguntar:

- ¿Cuántos perfiles necesitas?
- ¿Qué cargos son?
- ¿Qué nivel tienen?
- ¿Cuáles son las bandas salariales?
- ¿Tienes perfiles definidos?
- ¿Para cuándo necesitas cubrirlos?
- ¿Estarán en tu planilla o en la de un tercero?
- ¿Es una búsqueda puntual, volumen o RPO?

### Consulting

Preguntar:

- ¿Qué objetivo tiene el programa?
- ¿Cuántas personas participarán?
- ¿Qué niveles jerárquicos estarán incluidos?
- ¿Qué brechas o necesidades han identificado?
- ¿Será presencial, virtual o híbrido?
- ¿En qué ciudad o país se ejecutará?
- ¿Cuándo desean iniciar?

### Advisory

Preguntar:

- ¿Qué reto estratégico de talento quieren resolver?
- ¿Buscan diagnóstico, diseño, implementación o seguimiento?
- ¿Cuántas personas o áreas estarán involucradas?
- ¿Ya cuentan con información previa?
- ¿Qué decisiones esperan tomar con este proyecto?
- ¿Cuál es el plazo esperado?

---

## 17. Preguntas de prueba obligatorias

Prueba el agente con estas preguntas:

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
11. Necesito evaluar competencias de mis jefaturas, ¿qué servicio aplica?
12. Quiero diseñar mi cultura organizacional desde cero, ¿qué me recomiendas?

Pregunta fuera de alcance:

```text
¿Cuál es la política de vacaciones de AIMTALENT?
```

Respuesta esperada:

```text
No encontré información suficiente en la base documental disponible para responder con precisión.
```

---

## 18. README final esperado

Actualiza el README para que incluya:

1. Descripción del proyecto.
2. Objetivo.
3. Alcance V1.
4. Arquitectura RAG.
5. Estructura del repositorio.
6. Tecnologías utilizadas.
7. Branding aplicado.
8. Instalación local.
9. Variables de entorno.
10. Cómo ejecutar Streamlit.
11. Cómo reconstruir la base vectorial.
12. Ejemplos de preguntas.
13. Ejemplos de respuestas esperadas.
14. Reglas de seguridad documental.
15. Preparación para deploy en OCI.
16. Evidencia de funcionamiento.
17. Screenshots o ubicación para screenshots.
18. Próximos pasos.

---

## 19. Deploy en Oracle Cloud Infrastructure

No es necesario ejecutar el deploy si no hay credenciales, pero deja instrucciones claras.

Sugerencia de deploy:

- OCI Compute Instance.
- Python environment.
- Clonar repo desde GitHub.
- Instalar requirements.
- Configurar `.env`.
- Ejecutar Streamlit en puerto definido.
- Abrir puerto en Security List o NSG.
- Guardar captura o video en `assets/screenshots/` o `assets/demo/`.

Comando sugerido:

```bash
streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

Crear o actualizar:

```text
docs/deploy_oci.md
```

Debe explicar:

- Requisitos previos.
- Creación de instancia Compute.
- Clonación del repo.
- Instalación de dependencias.
- Configuración de variables.
- Ejecución de Streamlit.
- Apertura de puerto.
- Evidencia final para el challenge.

---

## 20. Requirements esperados

Actualiza `requirements.txt` según la implementación.

Base sugerida:

```text
streamlit
python-dotenv
pandas
chromadb
langchain
langchain-community
langchain-openai
openai
tiktoken
pytest
```

Si decides no usar LangChain para simplificar, puedes reducir dependencias, pero documenta la decisión.

---

## 21. Manejo de errores

La app debe manejar:

- Falta de API key.
- Carpeta `data/raw` vacía.
- Error al leer documentos.
- Vector store inexistente.
- Error al generar embeddings.
- Error de conexión con modelo.
- Pregunta fuera de alcance.

Nunca debe romperse con traceback visible para el usuario final. Puede mostrar mensajes amigables.

---

## 22. Criterios de aceptación

El proyecto se considera funcional si:

1. La app Streamlit abre correctamente.
2. El diseño usa branding AIMTALENT.
3. El usuario puede escribir una pregunta.
4. El sistema busca en la base documental limpia.
5. AimBot responde de forma coherente.
6. La respuesta se basa en documentos.
7. Se muestran fuentes utilizadas.
8. Si no hay respaldo, AimBot no inventa.
9. El README permite correr el proyecto localmente.
10. El proyecto está listo para subir a GitHub.
11. El proyecto tiene instrucciones para deploy en OCI.
12. El sistema no contiene nombres de clientes ni políticas internas.
13. La app puede reconstruir el índice vectorial.
14. La demo se ve presentable para evaluación.

---

## 23. Prioridad de implementación

Trabaja en este orden:

1. Revisar estructura actual.
2. Integrar base documental limpia.
3. Crear carpeta de branding y cargar assets si están disponibles.
4. Implementar document loader.
5. Implementar chunking.
6. Implementar vector store con ChromaDB.
7. Implementar retrieval.
8. Implementar prompt de AimBot.
9. Implementar generación de respuesta.
10. Mejorar Streamlit con branding.
11. Mostrar fuentes.
12. Agregar fallback.
13. Actualizar README.
14. Crear guía `docs/deploy_oci.md`.
15. Agregar pruebas básicas.
16. Validar preguntas obligatorias.
17. Preparar estructura lista para GitHub.

---

## 24. Comandos locales esperados

Instalación:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Crear `.env`:

```bash
cp .env.example .env
```

Ejecutar app:

```bash
streamlit run app/streamlit_app.py
```

---

## 25. Buenas prácticas de desarrollo

- Escribe código claro y mantenible.
- Evita sobreingeniería.
- Usa funciones pequeñas y comprensibles.
- Documenta decisiones relevantes.
- No hardcodees API keys.
- No subas `.env`.
- No subas vector store pesado si no es necesario.
- No incluyas documentos sensibles.
- Mantén el README actualizado.
- Prioriza una demo funcional y estable.

---

## 26. Entrega esperada

Al finalizar, el proyecto debe quedar con:

- Código funcional.
- App Streamlit operativa.
- Base documental limpia integrada.
- Vector store funcional.
- AimBot respondiendo con fuentes.
- Branding AIMTALENT aplicado.
- README actualizado.
- Guía de deploy en OCI.
- Pruebas básicas.
- Assets organizados.
- Estructura lista para GitHub.
- Evidencia preparada para captura o video.

---

## 27. Mensaje final esperado para el usuario del proyecto

Cuando el usuario use AimBot y quiera avanzar, puede cerrar así:

```text
Con esta información podemos orientar mejor la solución y preparar una propuesta más precisa.

Si deseas avanzar, puedo ayudarte a ordenar los datos clave del requerimiento para que el equipo de AIMTALENT lo revise con mayor agilidad.
```

---

## 28. Importante

No conviertas el proyecto en algo innecesariamente complejo.

El objetivo es un MVP sólido, claro, demostrable, bien documentado y visualmente alineado a AIMTALENT.

Prioriza:

1. Funcionamiento.
2. Claridad.
3. Trazabilidad.
4. Seguridad documental.
5. Experiencia visual profesional.
6. Facilidad de ejecución local.
7. Preparación para OCI.
