# Estructura de archivos — Challenge AIMTALENT

Este repositorio contiene los archivos base que deben subirse a GitHub para desarrollar el proyecto **AIMBOT Knowledge Agent**.

## Archivos principales

- `README.md`: documentación principal del proyecto.
- `CLAUDE.md`: guía completa para Claude Code.
- `requirements.txt`: dependencias del proyecto.
- `.env.example`: plantilla de variables de entorno.
- `.gitignore`: archivos que no deben subirse.

## Aplicación

- `app/streamlit_app.py`: interfaz inicial de Streamlit.

## Base documental limpia

Los documentos Markdown en `data/raw/` son la base de conocimiento limpia y anonimizada de AimBot.

No se deben subir documentos crudos, nombres de clientes, políticas internas, correos, teléfonos, RUC ni honorarios específicos.

## Código fuente

- `src/ingestion/document_loader.py`: lectura de documentos.
- `src/retrieval/vector_store.py`: base vectorial y recuperación.
- `src/generation/response_generator.py`: generación de respuesta.
- `src/config/settings.py`: configuración del proyecto.

## Branding

- `assets/branding/logo_aimtalent_principal.png`
- `assets/branding/isotipo_aimtalent_azul.png`
- `assets/branding/referencia_branding_aimtalent.png`

## Documentación adicional

- `docs/arquitectura.md`
- `docs/base_conocimiento.md`
- `docs/matriz_documental.md`
- `docs/matriz_documental_limpia_v1.csv`
- `docs/matriz_documental_aimbot_limpia_v1.xlsx`

## Evidencias futuras

- `assets/screenshots/`: capturas de la app funcionando.
- `assets/demo/`: video o evidencia del deploy.

## Importante

No subir `.env`, claves API, documentos sensibles ni vector store pesado si no es necesario.
