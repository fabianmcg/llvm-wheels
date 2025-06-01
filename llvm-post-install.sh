#!/bin/sh

LLVM_INSTALL_PATH=$1

rm -rv build_post_install
mkdir -v build_post_install
cd build_post_install
cmake ../llvm-post-install/ -DLLVM_INSTALL_PATH=${LLVM_INSTALL_PATH} -G Ninja
ninja
cd ..
rm -rv build_post_install

# Remove all symbolic links to libs.
find ${LLVM_INSTALL_PATH} -type l -name "*.so*" -exec rm -v {} \;
