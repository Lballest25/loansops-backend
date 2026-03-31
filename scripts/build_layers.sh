#!/usr/bin/env bash
# =============================================================
# build_layers.sh
# Builds both Lambda Layers before serverless deploy.
#
# Usage:
#   bash scripts/build_layers.sh
#
# Layers produced:
#   layers/dependencies/python/   ← pip packages
#   layers/shared/python/shared/  ← shared module
# =============================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo ">>> [1/2] Building dependencies layer..."
DEPS_DIR="$ROOT_DIR/layers/dependencies/python"
rm -rf "$DEPS_DIR"
mkdir -p "$DEPS_DIR"
pip install \
    --quiet \
    --requirement "$ROOT_DIR/requirements.txt" \
    --target "$DEPS_DIR"
echo "    Done — packages installed in layers/dependencies/python/"

echo ">>> [2/2] Building shared layer..."
SHARED_DST="$ROOT_DIR/layers/shared/python/shared"
rm -rf "$SHARED_DST"
mkdir -p "$(dirname "$SHARED_DST")"
cp -r "$ROOT_DIR/shared" "$SHARED_DST"
echo "    Done — shared module copied to layers/shared/python/shared/"

echo ">>> Layers built successfully."
