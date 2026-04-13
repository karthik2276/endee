#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# run.sh — Start the Endee server
#
# Usage:
#   chmod +x ./run.sh
#   ./run.sh
#   ./run.sh ndd_data_dir=./my_data
#   ./run.sh ndd_auth_token=your_secret_token
# ---------------------------------------------------------------------------

set -euo pipefail

NDD_DATA_DIR="${ndd_data_dir:-./data}"
NDD_AUTH_TOKEN="${ndd_auth_token:-}"

# Parse key=value arguments
for arg in "$@"; do
    key="${arg%%=*}"
    val="${arg#*=}"
    case "$key" in
        ndd_data_dir)    NDD_DATA_DIR="$val" ;;
        ndd_auth_token)  NDD_AUTH_TOKEN="$val" ;;
        *) echo "Unknown argument: $arg"; exit 1 ;;
    esac
done

# Find the binary
if [[ ! -L "./build/ndd" && ! -f "./build/ndd" ]]; then
    echo "Error: No binary found at ./build/ndd"
    echo "Run ./install.sh first."
    exit 1
fi

mkdir -p "$NDD_DATA_DIR"

echo "==> Starting Endee server..."
echo "    Data dir  : $NDD_DATA_DIR"
echo "    Auth token: ${NDD_AUTH_TOKEN:-<none>}"
echo "    Listening : http://localhost:8080"
echo ""

if [[ -n "$NDD_AUTH_TOKEN" ]]; then
    NDD_DATA_DIR="$NDD_DATA_DIR" NDD_AUTH_TOKEN="$NDD_AUTH_TOKEN" ./build/ndd
else
    NDD_DATA_DIR="$NDD_DATA_DIR" ./build/ndd
fi
