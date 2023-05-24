# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install llvm-qdpjit
#
# You can edit this file again by typing:
#
#     spack edit llvm-qdpjit
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class LlvmQdpjit(CMakePackage):
    """LLVM for QDP-JIT"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://llvm.org"
    git = "https://github.com/llvm/llvm-project"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("bjoo")

    # FIXME: Add proper versions here.
    version("15.x", branch="release/15.x")

    variant("targets", default="x86", description="The Architecture for LLVM", 
        values=("x86","powerpc","nvptx","amdgpu"), multi=True)

    root_cmakelists_dir = "llvm"
    def cmake_args(self):
        tgts=[]

        if "targets=x86" in self.spec:
            tgts.append("X86")
        if "targets=powerpc" in self.spec:
            tgts.append("PowerPC")
        if "targets=nvptx" in self.spec:
            tgts.append("NVPTX")
        if "target=amdgcn" in self.spec:
            tgts.append("AMDGCN")

        targets = ';'.join(tgts)
        print("Targets "+targets)

        try:
            build_type = self.spec.variants["build_type"].value
        except KeyError:
            build_type = "RelWithDebInfo"


        args = [ self.define("LLVM_ENABLE_TERMINFO", "OFF"),
                 self.define("CMAKE_BUILD_TYPE", build_type),
                 self.define("LLVM_ENABLE_ZLIB", "OFF"),
                 self.define("BUILD_SHARED_LIBS", "ON" ),
                 self.define("LLVM_TARGETS_TO_BUILD", targets) ]
        return args
