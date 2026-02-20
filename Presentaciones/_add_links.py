#!/usr/bin/env python3
"""Add GitHub Pages links to all presentation .md files."""
import os, re

BASE = r"C:\Users\freak\Preparacion Examenes\Presentaciones"

# Mapping: filename (without .md) → GitHub Pages URL
mapping = {
    "[JV-PI] Web Carolina Vega": "https://mutenros.github.io/Proyecto-intermodular-Web-Carolina-Vega/",
    "[Extra-BD] eID": "https://mutenros.github.io/eID/",
    "[Extra-BD] MenuSpreader": "https://mutenros.github.io/MenuSpreader/",
    "[Extra-ED] CuevasMotorSport": "https://mutenros.github.io/CuevasMotorSport/",
    "[Extra-LMSGI] Arraez-Portfolio": "https://mutenros.github.io/Arraez-Portfolio/",
    "[Extra-LMSGI] BA": "https://mutenros.github.io/BA/",
    "[Extra-LMSGI] BB": "https://mutenros.github.io/BB/",
    "[Extra-LMSGI] elece-barber": "https://mutenros.github.io/elece-barber/",
    "[Extra-LMSGI] Generador-de-Excusas-Premium": "https://mutenros.github.io/Generador-de-Excusas-Premium/",
    "[Extra-LMSGI] TokenMinimizer": "https://mutenros.github.io/TokenMinimizer/",
    "[Extra-PI] Espectaculos-Dani": "https://mutenros.github.io/Espectaculos-Dani/",
    "[Extra-PI] MutenRos.github.io": "https://mutenros.github.io/",
    "[Extra-PI] PrivateTenacitas": "https://mutenros.github.io/PrivateTenacitas/",
    "[Extra-PI] Tenacitas": "https://mutenros.github.io/Tenacitas/",
    "[Extra-PROG] Omni_ERP": "https://mutenros.github.io/Omni_ERP/",
    "[JV-BD] 001-Proyecto tienda online": "https://mutenros.github.io/Bases-de-datos-001-Proyecto-tienda-online/",
    "[JV-BD] 002-Proyecto IA para dietetica": "https://mutenros.github.io/Bases-de-datos-002-Proyecto-IA-para-diettica/",
    "[JV-ED] 001-Panel de administracion para proyecto juguetes": "https://mutenros.github.io/Entornos-001-Panel-de-administracin-para-proyecto-juguetes/",
    "[JV-ED] 002-HTML como pug": "https://mutenros.github.io/Entornos-002-HTML-como-pug/",
    "[JV-ED] 003-Recuperacion de emails con IMAP": "https://mutenros.github.io/Entornos-003-Recuperacin-de-emails-con-IMAP/",
    "[JV-ED] 004-Panel de control con GET y POST": "https://mutenros.github.io/Entornos-004-Panel-de-control-con-GET-y-POST/",
    "[JV-LMSGI] 001-Formateo y envio de emails": "https://mutenros.github.io/Lenguajes-de-marcas-001-Formateo-y-envo-de-emails/",
    "[JV-LMSGI] 002-Web curso IA": "https://mutenros.github.io/Lenguajes-de-marcas-002-Web-curso-IA/",
    "[JV-LMSGI] 003-Tienda de juguetes": "https://mutenros.github.io/Lenguajes-de-marcas-003-Tienda-de-juguetes/",
    "[JV-LMSGI] 004-Web-logos-Multiidioma": "https://mutenros.github.io/Lenguajes-de-marcas-004-Web-logos-Multiidioma/",
    "[JV-LMSGI] BI": "https://mutenros.github.io/BI/",
    "[JV-PI] 001-Proyecto Piero": "https://mutenros.github.io/Proyecto-intermodular-001-Proyecto-Piero/",
    "[JV-PI] 002-Primer contacto con PHP": "https://mutenros.github.io/Proyecto-intermodular-002-Primer-contacto-con-PHP/",
    "[JV-PI] 004-Proyecto ollama curriculums": "https://mutenros.github.io/Proyecto-intermodular-004-Proyecto-ollama-curriculums/",
    "[JV-PI] 005-Web con panel de control": "https://mutenros.github.io/Proyecto-intermodular-005-Web-con-panel-de-control/",
    "[JV-PI] 006-Creador de muchos articulos de blog": "https://mutenros.github.io/Proyecto-intermodular-006-creador-de-muchos-articulso-de-blog/",
    "[JV-PI] 007-Posicionamiento": "https://mutenros.github.io/Proyecto-intermodular-007-posicionamiento/",
    "[JV-PROG] 001-Proyecto-formularios-CRM": "https://mutenros.github.io/Programacion-001-Proyecto-formularios-CRM/",
    "[JV-PROG] 002-Panel-de-control-de-tienda-online": "https://mutenros.github.io/Programacion-002-Panel-de-control-de-tienda-online/",
    "[JV-PROG] 003-Proyecto SalvantallasNetflix": "https://mutenros.github.io/Programacion-003-Proyecto-SalvantallasNetflix/",
    "[JV-PROG] 004-IA inicial": "https://mutenros.github.io/Programacion-004-IA-inicial/",
    "[JV-PROG] 005-Entrenar IA": "https://mutenros.github.io/Programacion-005-Entrenar-IA/",
    "[JV-PROG] 007-Proyecto dibujantes": "https://mutenros.github.io/Programacion-007-Proyecto-dibujantes/",
    "[JV-SI] 001-Generacion de imagenes con IA": "https://mutenros.github.io/Sistemas-informaticos-001-Generacin-de-imgenes-con-IA/",
    "[JV-SI] 002-Panel de control con JVEstilo (Tailwind)": "https://mutenros.github.io/Sistemas-informaticos-002-Panel-de-control-con-JVEstilo-Tailwind/",
    "[JV-SI] 003-Mejora de la web curso IA": "https://mutenros.github.io/Sistemas-informaticos-003-Mejora-de-la-web-curso-IA/",
    "[JV-SI] 004-Mejora de la web de juguetes": "https://mutenros.github.io/Sistemas-informaticos-004-Mejora-de-la-web-de-juguetes/",
    "[JV-SI] HomeLab-Indexer": "https://mutenros.github.io/HomeLab-Indexer/",
}

link_line_template = "> 🔗 **GitHub Pages:** [{}]({})"

added = 0
already = 0
errors = []

for name, url in mapping.items():
    fpath = os.path.join(BASE, name + ".md")
    if not os.path.isfile(fpath):
        errors.append(f"NOT FOUND: {name}.md")
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if this GH Pages link is already present as a proper link line
    if f"**GitHub Pages:**" in content:
        already += 1
        print(f"  SKIP (already has link): {name}.md")
        continue

    link_line = link_line_template.format(url, url)

    # Strategy: insert the link line just before "## Introducción"
    # If there's a "---" separator right before it, insert before the "---"
    # Otherwise insert right before "## Introducción"

    # Find ## Introducción
    intro_match = re.search(r'\n(---\s*\n)?\s*\n## Introducción', content)
    if intro_match:
        insert_pos = intro_match.start()
        # Insert after whatever is at that position
        new_content = content[:insert_pos] + "\n\n" + link_line + content[insert_pos:]
    else:
        # Fallback: insert after line 3 (after image line)
        lines = content.split("\n")
        # Find first empty line after first image
        insert_idx = None
        for i, line in enumerate(lines):
            if i > 0 and line.startswith("!["):
                insert_idx = i + 1
                break
        if insert_idx is None:
            insert_idx = 2  # after title + blank line

        lines.insert(insert_idx, "")
        lines.insert(insert_idx + 1, link_line)
        new_content = "\n".join(lines)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

    added += 1
    print(f"  ✓ {name}.md")

print(f"\nResultado: {added} añadidos, {already} ya tenían, {len(errors)} errores")
for e in errors:
    print(f"  ⚠ {e}")
