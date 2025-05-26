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
