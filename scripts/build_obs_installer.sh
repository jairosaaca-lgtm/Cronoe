#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="$ROOT_DIR/.build_obs_installer"
DIST_DIR="$ROOT_DIR/dist"
APP_NAME="cronoe_obs_installer.pyz"

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR" "$DIST_DIR"

cp "$ROOT_DIR/tools/obs_plugin_installer.py" "$BUILD_DIR/__main__.py"
python3 -m zipapp "$BUILD_DIR" -o "$DIST_DIR/$APP_NAME" -p "/usr/bin/env python3"
chmod +x "$DIST_DIR/$APP_NAME"

echo "✅ Generado: $DIST_DIR/$APP_NAME"
