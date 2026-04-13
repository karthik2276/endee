cmake_minimum_required(VERSION 3.20)
project(endee VERSION 1.3.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ---------------------------------------------------------------------------
# Build options
# ---------------------------------------------------------------------------
option(USE_AVX2   "Enable AVX2 SIMD optimizations"   OFF)
option(USE_AVX512 "Enable AVX-512 SIMD optimizations" OFF)
option(USE_NEON   "Enable ARM NEON optimizations"     OFF)
option(USE_SVE2   "Enable ARM SVE2 optimizations"     OFF)
option(DEBUG      "Enable full debug symbols"         OFF)
option(ND_DEBUG   "Enable Endee internal debug logs"  OFF)

# ---------------------------------------------------------------------------
# Compiler flags
# ---------------------------------------------------------------------------
set(COMPILE_FLAGS "")

if(USE_AVX2)
    list(APPEND COMPILE_FLAGS -mavx2 -mfma)
    set(NDD_BINARY_NAME "ndd-avx2")
elseif(USE_AVX512)
    list(APPEND COMPILE_FLAGS -mavx512f -mavx512bw -mavx512vl -mfma)
    set(NDD_BINARY_NAME "ndd-avx512")
elseif(USE_NEON)
    if(APPLE)
        set(NDD_BINARY_NAME "ndd-neon-darwin")
    else()
        set(NDD_BINARY_NAME "ndd-neon")
    endif()
elseif(USE_SVE2)
    list(APPEND COMPILE_FLAGS -march=armv9-a+sve2)
    set(NDD_BINARY_NAME "ndd-sve2")
else()
    message(FATAL_ERROR
        "No SIMD target specified. Pass one of:\n"
        "  -DUSE_AVX2=ON  (Intel/AMD)\n"
        "  -DUSE_AVX512=ON (server-grade Intel/AMD)\n"
        "  -DUSE_NEON=ON  (Apple Silicon / ARM)\n"
        "  -DUSE_SVE2=ON  (ARMv9)\n"
    )
endif()

if(DEBUG)
    list(APPEND COMPILE_FLAGS -g3 -O0)
else()
    list(APPEND COMPILE_FLAGS -O3)
endif()

if(ND_DEBUG)
    list(APPEND COMPILE_FLAGS -DND_DEBUG)
endif()

# ---------------------------------------------------------------------------
# Source files
# ---------------------------------------------------------------------------
file(GLOB_RECURSE NDD_SOURCES
    "${CMAKE_SOURCE_DIR}/src/*.cpp"
)

# ---------------------------------------------------------------------------
# Executable
# ---------------------------------------------------------------------------
add_executable(${NDD_BINARY_NAME} ${NDD_SOURCES})

target_compile_options(${NDD_BINARY_NAME} PRIVATE ${COMPILE_FLAGS})

target_include_directories(${NDD_BINARY_NAME} PRIVATE
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/third_party
)

find_package(OpenSSL REQUIRED)
find_package(CURL REQUIRED)

target_link_libraries(${NDD_BINARY_NAME} PRIVATE
    OpenSSL::SSL
    OpenSSL::Crypto
    CURL::libcurl
    pthread
)

message(STATUS "Endee ${PROJECT_VERSION} — binary: ${NDD_BINARY_NAME}")
