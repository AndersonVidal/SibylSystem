#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

TEMPLATE="$PROJECT_DIR/resources/macos/Sibyl.command"
DEST_DIR="$HOME/Applications"
DEST="$DEST_DIR/Sibyl.command"

echo "Instalando launcher do Sibyl..."

mkdir -p "$DEST_DIR"

sed "s|SIBYL_PROJECT_DIR|$PROJECT_DIR|g" "$TEMPLATE" > "$DEST"
chmod +x "$DEST"

echo ""
echo "Launcher instalado em: $DEST"
echo ""
echo "Clique duas vezes em 'Sibyl.command' no Finder para iniciar."
echo ""
echo "Para remover o launcher:"
echo "  rm \"$DEST\""
echo ""
echo "Para reinstalar após mover o projeto de diretório:"
echo "  ./scripts/install-launcher-macos.sh"
