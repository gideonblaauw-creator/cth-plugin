#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 generate.py
python3 render.py
python3 audit_text.py
pdfinfo dataton-preguntas-espacios.pdf | grep -E 'Pages|Page size'
pdffonts dataton-preguntas-espacios.pdf
sha256sum dataton-preguntas-espacios.pdf