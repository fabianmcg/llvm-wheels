cmake_minimum_required(VERSION 3.20)
project(llvm VERSION 24)

# ===----------------------------------------------------------------------=== #
# Configurable flags
# ===----------------------------------------------------------------------=== #

set(LLVM_TARGETS_TO_BUILD "Native,X86,NVPTX,AMDGPU," CACHE STRING "LLVM_TARGETS_TO_BUILD")
set(LLVM_ENABLE_LLD ON CACHE BOOL "LLVM_ENABLE_LLD")
set(LLVM_CCACHE_BUILD ON CACHE BOOL "LLVM_CCACHE_BUILD")
set(LLVM_ENABLE_ASSERTIONS ON CACHE BOOL "LLVM_ENABLE_ASSERTIONS")
set(MLIR_ENABLE_BINDINGS_PYTHON ON CACHE BOOL "MLIR_ENABLE_BINDINGS_PYTHON")
set(LLVM_DYLIB ON CACHE BOOL "LLVM_DYLIB")

# ===----------------------------------------------------------------------=== #
# Configurable but better not to touch:
# ===----------------------------------------------------------------------=== #

set(LLVM_ENABLE_PROJECTS "clang,mlir,lld," CACHE STRING "LLVM_ENABLE_PROJECTS")
set(LLVM_DISTRIBUTION_COMPONENTS "LLVM,LLVMSupport,LLVMDemangle,llvm-headers,cmake-exports,FileCheck,llvm-link,llvm-config,not,count,MLIR,MLIR-C,mlir-headers,mlir-cmake-exports,mlir-tblgen,mlir-opt,mlir-lsp-server,mlir-runner,mlir-translate,MLIRPythonModules,mlir-python-sources,clang,clang-cpp,clang-cmake-exports,clang-resource-headers,clang-format,clang-linker-wrapper,lld,lld-cmake-exports," CACHE STRING "LLVM_DISTRIBUTION_COMPONENTS")
set(LLVM_INSTALL_UTILS ON CACHE BOOL "LLVM_INSTALL_UTILS")

set(LLVM_INSTALL_PATH ${CMAKE_INSTALL_PREFIX}/llvm CACHE PATH "LLVM_INSTALL_PATH")

# ===----------------------------------------------------------------------=== #
# LLVM CMake arguments
# ===----------------------------------------------------------------------=== #

if(APPLE)
  set(origin_token "@loader_path")
else()
  set(origin_token "\$ORIGIN")
endif()

set(LLVM_CMAKE_ARGS
  -DCMAKE_BUILD_TYPE=Release
  -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
  -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
  -DLLVM_ENABLE_PROJECTS=${LLVM_ENABLE_PROJECTS}
  -DLLVM_TARGETS_TO_BUILD=${LLVM_TARGETS_TO_BUILD}
  -DCMAKE_INSTALL_PREFIX=${LLVM_INSTALL_PATH}
  -DLLVM_ENABLE_LLD=${LLVM_ENABLE_LLD}
  -DLLVM_CCACHE_BUILD=${LLVM_CCACHE_BUILD}
  -DLLVM_INSTALL_UTILS=${LLVM_INSTALL_UTILS}
  -DLLVM_ENABLE_ASSERTIONS=${LLVM_ENABLE_ASSERTIONS}
  -DLLVM_APPEND_VC_REV=ON
  -DLLVM_BUILD_LLVM_DYLIB=${LLVM_DYLIB}
  -DLLVM_LINK_LLVM_DYLIB=${LLVM_DYLIB}
  -DMLIR_LINK_MLIR_DYLIB=${LLVM_DYLIB}
  -DMLIR_BUILD_MLIR_C_DYLIB=${LLVM_DYLIB}
  -DMLIR_ENABLE_BINDINGS_PYTHON=${MLIR_ENABLE_BINDINGS_PYTHON}
  -DLLVM_DISTRIBUTION_COMPONENTS=${LLVM_DISTRIBUTION_COMPONENTS}
  -DLLVM_ENABLE_LIBXML2=OFF
  -DLLVM_ENABLE_ZLIB=OFF
  -DLLVM_ENABLE_LIBEDIT=OFF
  -DLLVM_ENABLE_ZSTD=OFF
  -DLLVM_ENABLE_LIBCXX=OFF
  -DLLVM_ENABLE_TERMINFO=OFF
  -DCMAKE_SKIP_BUILD_RPATH=OFF
  -DBUILD_RPATH_USE_ORIGIN=ON
  -DCMAKE_INSTALL_RPATH=${origin_token},${origin_token}/../lib
  -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=OFF
  -DMLIR_INCLUDE_TESTS=OFF
  -DPython3_EXECUTABLE=${PYTHON_EXECUTABLE}
  -DPython_EXECUTABLE=${PYTHON_EXECUTABLE}
)

message(WARNING "${LLVM_CMAKE_ARGS}")

# ===----------------------------------------------------------------------=== #
# Configure LLVM
# ===----------------------------------------------------------------------=== #

string(REPLACE "," " " LLVM_CMAKE_TARGETS "${LLVM_DISTRIBUTION_COMPONENTS}")
separate_arguments(LLVM_CMAKE_TARGETS NATIVE_COMMAND "${LLVM_CMAKE_TARGETS}")

include(ExternalProject)
ExternalProject_add(build-llvm
  SOURCE_DIR ${CMAKE_SOURCE_DIR}/llvm-project/llvm
  BINARY_DIR ${CMAKE_BINARY_DIR}/llvm-build
  UPDATE_COMMAND ""
  INSTALL_COMMAND ninja install-distribution
  USES_TERMINAL_CONFIGURE 1
  USES_TERMINAL_BUILD 1
  LIST_SEPARATOR ","
  CMAKE_ARGS ${LLVM_CMAKE_ARGS}
  BUILD_COMMAND cmake --build . --target ${LLVM_CMAKE_TARGETS}
)
