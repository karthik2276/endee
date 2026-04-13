#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# install.sh — Build Endee from source (Linux / macOS only)
#
# Usage:
#   chmod +x ./install.sh
#   ./install.sh --release --avx2     # Intel/AMD Linux
#   ./install.sh --release --neon     # Apple Silicon Mac
#   ./install.sh --release --avx512   # Server-grade Xeon/EPYC
#   ./install.sh --release --sve2     # ARMv9 ARM server
# ---------------------------------------------------------------------------

set -euo pipefail

BUILD_MODE=""
CPU_FLAG=""

# ---------- Parse arguments ----------
for arg in "$@"; do
    case "$arg" in
        --release)    BUILD_MODE="Release" ;;
        --debug_all)  BUILD_MODE="Debug" ;;
        --debug_nd)   BUILD_MODE="RelWithDebInfo" ;;
        --avx2)       CPU_FLAG="USE_AVX2" ;;
        --avx512)     CPU_FLAG="USE_AVX512" ;;
        --neon)       CPU_FLAG="USE_NEON" ;;
        --sve2)       CPU_FLAG="USE_SVE2" ;;
        *)            echo "Unknown argument: $arg"; exit 1 ;;
    esac
done

if [[ -z "$BUILD_MODE" ]]; then
    echo "Error: build mode required. Use --release, --debug_all, or --debug_nd"
    exit 1
fi

if [[ -z "$CPU_FLAG" ]]; then
    echo "Error: CPU flag required. Use --avx2, --avx512, --neon, or --sve2"
    exit 1
fi

echo "==> Build mode : $BUILD_MODE"
echo "==> CPU target : $CPU_FLAG"

# ---------- Detect OS ----------
OS="$(uname -s)"
case "$OS" in
    Linux*)  echo "==> OS: Linux" ;;
    Darwin*) echo "==> OS: macOS" ;;
    *)
        echo "Unsupported OS: $OS"
        echo "Windows users: use Docker (Method 1 or 2) — see docs/getting-started.md"
        exit 1
        ;;
esac

# ---------- Install dependencies ----------
echo "==> Installing build dependencies..."
if [[ "$OS" == "Linux" ]]; then
    sudo apt-get update -qq
    sudo apt-get install -y \
        build-essential \
        cmake \
        clang-19 \
        libssl-dev \
        libcurl4-openssl-dev \
        git \
        curl

    export CC=clang-19
    export CXX=clang++-19
elif [[ "$OS" == "Darwin" ]]; then
    brew install cmake openssl curl llvm
    LLVM_PATH="$(brew --prefix llvm)"
    export CC="$LLVM_PATH/bin/clang"
    export CXX="$LLVM_PATH/bin/clang++"
fi

# ---------- CMake configure + build ----------
echo "==> Configuring CMake..."
mkdir -p build && cd build

cmake \
    -DCMAKE_BUILD_TYPE="$BUILD_MODE" \
    "-D${CPU_FLAG}=ON" \
    ..

echo "==> Building ($(nproc 2>/dev/null || sysctl -n hw.logicalcpu) cores)..."
make -j"$(nproc 2>/dev/null || sysctl -n hw.logicalcpu)"

cd ..

echo ""
echo "==========================================================="
echo " Build complete! Run the server with:"
echo "   chmod +x ./run.sh"
echo "   ./run.sh"
echo "==========================================================="
