# Base de Conocimiento Limpia V1 — AIMBOT Knowledge Agent

## Propósito
Esta base de conocimiento fue curada para alimentar una primera versión comercial y consultiva de AimBot, el agente de IA de AIMTALENT.

AimBot debe ayudar a diagnosticar necesidades de clientes o prospectos, explicar los servicios de AIMTALENT, orientar la conversación hacia la unidad de negocio correspondiente y recoger información suficiente para acelerar la elaboración de una propuesta comercial.

## Alcance
Incluye únicamente información comercial, institucional, metodológica y de diagnóstico relacionada con las unidades de negocio de AIMTALENT:

- Executive Search
- Hiring Solutions
- Consulting
- Advisory

## Exclusiones aplicadas
No se incluyen:
- Nombres de clientes.
- Políticas internas de colaboradores.
- Correos electrónicos personales o corporativos de personas específicas.
- Teléfonos personales.
- RUC de clientes o proveedores.
- Honorarios cerrados por cliente.
- Logos o referencias identificables de clientes.
- Comentarios internos de trabajo.
- Información administrativa no necesaria para una conversación comercial.

## Uso recomendado en RAG
Cada archivo está escrito en formato Markdown, con títulos claros y secciones separadas para facilitar la segmentación en chunks y la recuperación semántica.

## Reglas de respuesta esperadas del agente
AimBot debe:
1. Responder solo con base en esta base documental.
2. Mantener un tono ejecutivo, cálido, consultivo y persuasivo.
3. Hacer preguntas de diagnóstico antes de recomendar una solución.
4. No inventar datos si la información no está disponible.
5. Solicitar correo corporativo y datos mínimos de contacto antes de cerrar una derivación comercial.
6. Evitar entregar precios cerrados si no existe una propuesta validada.
