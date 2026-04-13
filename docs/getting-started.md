**Endee** is a specialized, high-performance vector database built for speed and efficiency — engineered for production AI systems that need to process data at scale.

Never heard of a vector database? No worries — check out our blog where we explain what it is and what you can build with it: [endee.io/blog](https://endee.io/blog)

---

To use Endee, the first step is to start the server. There are 4 ways to do this:

1. **Docker** — pull and run the pre-built image from Docker Hub
2. **Docker build from source** — build the Docker image yourself from the source code (recommended)
3. **install.sh script** — automated build script for Linux and macOS
4. **Manual CMake build** — full manual control over the build

> **Windows users:** Methods 3 and 4 are not supported on Windows. Docker (Methods 1 or 2) is the only way to run Endee on Windows.

---

### Prerequisite: Install Docker

That's the only thing you need. Go to [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/) and install Docker Desktop for your OS (Windows, Mac, or Linux).

Once installed, open a terminal and verify it works:

```bash
docker --version
```

---

## Method 1: Docker (Pull Pre-built Image)

```bash
docker run \
  --ulimit nofile=100000:100000 \
  -p 8080:8080 \
  -v ./endee-data:/data \
  --name endee-server \
  --restart unless-stopped \
  endeeio/endee-server:latest
```

The server starts at **[http://localhost:8080](http://localhost:8080)**.

---

## Method 2: Docker Build from Source

### Step 1: Figure out your CPU type

| Your hardware | Flag to use |
|---|---|
| Mac with M1 / M2 / M3 / M4 chip | `neon` |
| Linux or Windows with Intel or AMD CPU | `avx2` |
| Server-grade Intel Xeon / AMD EPYC | `avx512` |
| ARM server (ARMv9) | `sve2` |

### Step 2: Build the image

```bash
# Intel/AMD (x86_64)
docker build \
  --ulimit nofile=100000:100000 \
  --build-arg BUILD_ARCH=avx2 \
  -t endee-oss:latest \
  -f ./infra/Dockerfile \
  .
```

### Step 3: Run with Docker Compose

```bash
docker compose up -d
```

---

## Method 3: install.sh (Linux / macOS)

```bash
chmod +x ./install.sh ./run.sh
./install.sh --release --avx2
./run.sh
```

The server starts at **[http://localhost:8080](http://localhost:8080)**.

---

## Method 4: Manual CMake Build

```bash
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DUSE_AVX2=ON ..
make -j$(nproc)
cd ..
mkdir -p ./data
NDD_DATA_DIR=./data ./build/ndd
```

---

## Verify it's running

```bash
curl http://localhost:8080/api/v1/health
```

---

## Next Steps

Once your server is running, head over to [docs.endee.io/quick-start](https://docs.endee.io/quick-start) to learn how to create indexes, store vectors, and run your first similarity search.
