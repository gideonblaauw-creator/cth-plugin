#!/usr/bin/env bash
# Create tools/quarto/.venv with pinned requirements.txt.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"

if [[ -d "$VENV" ]]; then
  echo "Python venv exists at $VENV"
else
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --upgrade pip wheel
  "$VENV/bin/pip" install -r "$ROOT/requirements.txt"
  "$VENV/bin/python" -m ipykernel install --user --name=cth-quarto --display-name "CTH Quarto (tools/quarto)"
  echo "Created venv and registered ipykernel cth-quarto"
fi

"$VENV/bin/python" -c "import pandas, plotly, itables; print('OK:', pandas.__version__, plotly.__version__)"
