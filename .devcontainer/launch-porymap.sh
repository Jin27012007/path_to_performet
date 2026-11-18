#!/usr/bin/env bash
set -euo pipefail
export DISPLAY=:1
export QT_X11_NO_MITSHM=1
BIN="$HOME/.local/opt/porymap/porymap"
if [ ! -x "$BIN" ]; then
  echo "Porymap ainda não foi compilado. Execute: bash .devcontainer/setup-porymap.sh" >&2
  exit 1
fi
exec "$BIN" "$PWD"
