from __future__ import annotations
from pathlib import Path as _Path
from dataclasses import (
    dataclass as _dataclass,
    field as _field,
    fields as _fields,
)
from subprocess import run as _run

import sys as _sys

from ._version import version as LLVM_VERSION
from .llvm_version import *

__version__ = LLVM_VERSION


def root_path() -> _Path:
    """Returns the root path of the package"""
    return _Path(__file__).parent


def bin_path() -> _Path:
    """Returns the binary path"""
    return root_path() / "bin"


def lib_path() -> _Path:
    """Returns the library path"""
    return root_path() / "lib"


def llvm_lib_path(name: str) -> _Path:
    """Returns the library path"""
    return root_path() / _Path("lib", f"lib{name}.so.{LLVM_SONAME_SUFFIX}")


def cmake_path() -> _Path:
    """Returns the cmake path"""
    return lib_path() / "cmake"


def mlir_python_root_path() -> _Path:
    """Returns the mlir root path"""
    return root_path() / _Path("python_packages", "mlir_core")


# Add the MLIR package to the path
_sys.path.append(str(mlir_python_root_path()))


@_dataclass
class LLVMTool:
    """Class for storing an LLVM tool"""

    name: str

    def get_path(self) -> _Path:
        """Returns the path of the tool"""
        return bin_path() / self.name

    def invoke(self, *args, **kwargs):
        return _run(args=[self.get_path()] + list(args), **kwargs)

    def __str__(self) -> str:
        return f"LLVMTool(name='{self.name}', path=`{self.get_path()}`)"

    def __repr__(self):
        return str(self)


def get_tool(name: str) -> LLVMTool:
    return LLVMTool(name)


def _get_tool_field(name: str) -> _field:
    return _field(default_factory=lambda: get_tool(name))


@_dataclass(frozen=True)
class LLVMTools:
    """The collection of LLVM tools in this distribution."""

    llvm_config: LLVMTool = _get_tool_field("llvm-config")
    FileCheck: LLVMTool = _get_tool_field("FileCheck")
    llvm_link: LLVMTool = _get_tool_field("llvm-link")
    llvm_not: LLVMTool = _get_tool_field("not")
    llvm_count: LLVMTool = _get_tool_field("count")
    clang: LLVMTool = _get_tool_field("clang")
    clang_cpp: LLVMTool = _get_tool_field("clang++")
    clang_format: LLVMTool = _get_tool_field("clang-format")
    mlir_tblgen: LLVMTool = _get_tool_field("mlir-tblgen")
    mlir_opt: LLVMTool = _get_tool_field("mlir-opt")
    mlir_runner: LLVMTool = _get_tool_field("mlir-runner")
    mlir_translate: LLVMTool = _get_tool_field("mlir-translate")

    def astuple(self) -> tuple:
        return tuple(getattr(self, field.name) for field in _fields(self))

    def asdict(self) -> dict:
        return {v.name: v for v in self.astuple()}


def get_tools() -> LLVMTools:
    return LLVMTools()


def _cli() -> int:
    import argparse as _argparse

    parser = _argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--root-path", action="store_true", help="Prints the root path"
    )
    group.add_argument(
        "--bin-path", action="store_true", help="Prints the bin path"
    )
    group.add_argument(
        "--lib-path", action="store_true", help="Prints the bin path"
    )
    group.add_argument(
        "--cmake-path", action="store_true", help="Prints the cmake path"
    )
    group.add_argument(
        "--tools", action="store_true", help="Prints the available tools"
    )
    group.add_argument(
        "--tool-path", type=str, default="", help="Prints the tool path"
    )
    group.add_argument(
        "--library-path", type=str, default="", help="Prints a library path"
    )
    args = parser.parse_args()
    if args.root_path:
        print(str(root_path()))
        return 0
    if args.bin_path:
        print(str(bin_path()))
        return 0
    if args.lib_path:
        print(str(lib_path()))
        return 0
    if args.cmake_path:
        print(str(cmake_path()))
        return 0
    tools = get_tools().asdict()
    if args.tools:
        print("\n".join(map(lambda x: "  " + str(x), tools.values())))
        return 0
    if args.tool_path:
        print(LLVMTool(args.tool_path).get_path())
    if args.library_path:
        print(str(llvm_lib_path(args.library_path)))

    return 0


def cli():
    raise SystemExit(_cli())
