"""
Carga documental y chunking de la base de conocimiento limpia de AIMTALENT.
Lee archivos Markdown desde data/raw y los divide en fragmentos con metadata.
"""

from pathlib import Path

from src.config import settings

# Categoría inferida desde el nombre del archivo de la base limpia
CATEGORY_MAP = {
    "00_readme_base_conocimiento": "Base de conocimiento",
    "01_institucional_aimtalent": "Institucional",
    "02_aimbot_comportamiento": "Comportamiento AimBot",
    "03_executive_search": "Executive Search",
    "04_hiring_solutions": "Hiring Solutions",
    "05_consulting": "Consulting",
    "06_advisory": "Advisory",
    "07_metodologia_y_trazabilidad": "Metodología y trazabilidad",
    "08_checklist_diagnostico_propuesta": "Diagnóstico comercial",
    "09_matriz_documental_limpia": "Matriz documental",
}


def infer_category(filename: str) -> str:
    """Infiere la categoría documental desde el nombre del archivo."""
    stem = Path(filename).stem.lower()
    if stem in CATEGORY_MAP:
        return CATEGORY_MAP[stem]
    return stem.replace("_", " ").strip().title() or "General"


def load_markdown_documents(folder_path: str | None = None) -> list[dict]:
    """Carga los documentos Markdown de la base limpia con su metadata."""
    path = Path(folder_path or settings.DOCUMENTS_PATH)
    if not path.exists():
        return []

    documents = []
    for file in sorted(path.glob("*.md")):
        content = file.read_text(encoding="utf-8").strip()
        if not content:
            continue
        documents.append(
            {
                "content": content,
                "metadata": {
                    "source": file.name,
                    "category": infer_category(file.name),
                },
            }
        )
    return documents


def _split_section(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Divide un texto en fragmentos por párrafos, respetando tamaño y overlap."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= chunk_size:
            current = candidate
            continue
        if current:
            chunks.append(current)
            # Conserva la cola del chunk anterior como overlap
            current = (current[-overlap:] + "\n\n" + paragraph).strip() if overlap else paragraph
        else:
            current = paragraph
        # Párrafos individuales más largos que chunk_size se cortan duro
        while len(current) > chunk_size:
            chunks.append(current[:chunk_size])
            current = current[chunk_size - overlap:].strip() if overlap else current[chunk_size:].strip()

    if current:
        chunks.append(current)
    return chunks


def chunk_documents(
    documents: list[dict],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[dict]:
    """
    Divide los documentos en chunks conservando fuente, categoría,
    sección (último encabezado Markdown) y número de chunk.
    """
    chunk_size = chunk_size or settings.CHUNK_SIZE
    chunk_overlap = chunk_overlap if chunk_overlap is not None else settings.CHUNK_OVERLAP

    all_chunks = []
    for doc in documents:
        # Separa el documento por encabezados para conservar la sección
        sections: list[tuple[str, list[str]]] = []
        current_title = doc["metadata"]["category"]
        current_lines: list[str] = []
        for line in doc["content"].splitlines():
            if line.lstrip().startswith("#"):
                if current_lines:
                    sections.append((current_title, current_lines))
                current_title = line.lstrip("# ").strip() or current_title
                current_lines = [line]
            else:
                current_lines.append(line)
        if current_lines:
            sections.append((current_title, current_lines))

        # Agrupa secciones pequeñas y corta las grandes
        chunk_number = 0
        buffer_text = ""
        buffer_section = sections[0][0] if sections else current_title

        def flush(text: str, section: str) -> None:
            nonlocal chunk_number
            for piece in _split_section(text, chunk_size, chunk_overlap):
                chunk_number += 1
                all_chunks.append(
                    {
                        "content": piece,
                        "metadata": {
                            "source": doc["metadata"]["source"],
                            "category": doc["metadata"]["category"],
                            "section": section,
                            "chunk_number": chunk_number,
                        },
                    }
                )

        for title, lines in sections:
            section_text = "\n".join(lines).strip()
            if not section_text:
                continue
            candidate = f"{buffer_text}\n\n{section_text}".strip() if buffer_text else section_text
            if len(candidate) <= chunk_size:
                buffer_text = candidate
                continue
            if buffer_text:
                flush(buffer_text, buffer_section)
            buffer_text = section_text
            buffer_section = title
        if buffer_text:
            flush(buffer_text, buffer_section)

    return all_chunks
