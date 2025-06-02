# LLVM(MLIR) distribution as (manylinux-compatible) wheel

Project inspired by and derived from https://github.com/makslevental/mlir-wheels/tree/main, and also accomplished with guidance from @makslevental (this is not an endorsement by Maks).

Status: not even alpha
Support: Linux and MacOS

### Building
#### Linux
```bash
python3 -m venv .build_venv
. .build_venv/bin/activate
pip install cibuildwheel
cibuildwheel "$HERE" --platform linux
```


### Usage

#### Command line:
The wheel provides the `llvm` cmd utility for obtaining misc information:

```bash
usage: llvm [-h] [--root-path | --bin-path | --lib-path | --cmake-path | --tools | --tool-path TOOL_PATH | --library-path LIBRARY_PATH]

options:
  -h, --help            show this help message and exit
  --root-path           Prints the root path
  --bin-path            Prints the bin path
  --lib-path            Prints the bin path
  --cmake-path          Prints the cmake path
  --tools               Prints the available tools
  --tool-path TOOL_PATH
                        Prints the tool path
  --library-path LIBRARY_PATH
                        Prints a library path
```

##### Example:
```bash
llvm --cmake-path
# Prints:
${HOME}/.llvm/lib/python3.11/site-packages/llvm/lib/cmake
```

### Python

For python always load the `llvm` module before using `mlir` ie:

```python
import llvm

from mlir import ir

# For only loading the shared libs and make them visible use:
import llvm.mlir_lib   # For MLIR
import llvm.mlir_c_lib # For MLIR-C
import llvm.llvm_lib   # For MLIR
```
