#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

TEMPLATE="$PROJECT_DIR/resources/linux/sibyl.desktop"
DEST_DIR="$HOME/.local/share/applications"
DEST="$DEST_DIR/sibyl.desktop"

echo "Instalando launcher do Sibyl..."

mkdir -p "$DEST_DIR"

sed "s|SIBYL_PROJECT_DIR|$PROJECT_DIR|g" "$TEMPLATE" > "$DEST"

echo ""
echo "Launcher instalado em: $DEST"
echo ""
echo "O Sibyl deve aparecer no menu de aplicações em instantes."
echo ""
echo "Para remover o launcher:"
echo "  rm $DEST"
echo ""
echo "Para reinstalar após mover o projeto de diretório:"
echo "  ./scripts/install-launcher-linux.sh"
