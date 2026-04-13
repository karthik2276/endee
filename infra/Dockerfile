FROM ubuntu:22.04 AS builder

ARG BUILD_ARCH=avx2

RUN apt-get update -qq && apt-get install -y \
    build-essential \
    cmake \
    clang-19 \
    libssl-dev \
    libcurl4-openssl-dev \
    git \
    curl \
 && rm -rf /var/lib/apt/lists/*

ENV CC=clang-19
ENV CXX=clang++-19

WORKDIR /app
COPY . .

RUN mkdir -p build && cd build && \
    case "$BUILD_ARCH" in \
        avx2)   cmake -DCMAKE_BUILD_TYPE=Release -DUSE_AVX2=ON   .. ;; \
        avx512) cmake -DCMAKE_BUILD_TYPE=Release -DUSE_AVX512=ON .. ;; \
        neon)   cmake -DCMAKE_BUILD_TYPE=Release -DUSE_NEON=ON   .. ;; \
        sve2)   cmake -DCMAKE_BUILD_TYPE=Release -DUSE_SVE2=ON   .. ;; \
        *)      echo "Unknown BUILD_ARCH: $BUILD_ARCH" && exit 1 ;; \
    esac && \
    make -j$(nproc)

# ---------------------------------------------------------------------------
FROM ubuntu:22.04 AS runtime

RUN apt-get update -qq && apt-get install -y \
    libssl3 \
    libcurl4 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/build/ndd ./ndd

RUN mkdir -p /data

ENV NDD_DATA_DIR=/data
ENV NDD_NUM_THREADS=0
ENV NDD_AUTH_TOKEN=""

EXPOSE 8080

CMD ["./ndd"]
