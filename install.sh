#!/bin/sh
# xvidlink installer - symlinks the command into ~/.local/bin
set -e

SRC="$(cd "$(dirname "$0")" && pwd)/xvidlink.py"
DEST="$HOME/.local/bin/xvidlink"

mkdir -p "$HOME/.local/bin"
ln -sf "$SRC" "$DEST"

echo "installed: xvidlink -> $DEST"
echo "run 'xvidlink <url>' from anywhere"
