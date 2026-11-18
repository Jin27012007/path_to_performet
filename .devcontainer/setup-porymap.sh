#!/usr/bin/env bash
set -euo pipefail

SRC="$HOME/.local/src/porymap"
BUILD="$HOME/.local/opt/porymap"

mkdir -p "$HOME/.local/src" "$BUILD"
if [ ! -d "$SRC/.git" ]; then
  git clone https://github.com/huderlem/porymap.git "$SRC"
else
  git -C "$SRC" fetch --tags origin
fi

# Pin to the upstream revision reviewed for this Codespaces setup.
git -C "$SRC" checkout 26b919d7ff4b54152de010abd5bf344af2ebe116

cd "$SRC"
qmake6 porymap.pro -o Makefile
make -j2
install -m 0755 porymap "$BUILD/porymap"

cat > "$HOME/.local/bin-porymap" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
export QT_X11_NO_MITSHM=1
exec "$HOME/.local/opt/porymap/porymap" "$@"
EOF
chmod +x "$HOME/.local/bin-porymap"

echo "Porymap compilado em $BUILD/porymap"
