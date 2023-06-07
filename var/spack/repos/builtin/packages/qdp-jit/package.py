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
#     spack install qdp-jit
#
# You can edit this file again by typing:
#
#     spack edit qdp-jit
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class QdpJit(CMakePackage,CudaPackage,ROCmPackage):
    """QDP-JIT: The JIT version of the QDP++ Software layer"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://jeffersonlab.github.io/qdp-jit"
    git = "https://github.com/jeffersonlab/qdp-jit.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("bjoo", "fwinter")

    # FIXME: Add proper versions here.
    version("devel", branch="devel", submodules=True)

    # FIXME: Add dependencies if required.
    depends_on("libxml2")
    depends_on("llvm-qdpjit@15.x", when="+cuda")
    depends_on("llvm-amdgpu", when="+rocm")

    variant("parallel_arch", default="parscalar", description="QDPXX Parallel arch",
            values=("scalar", "parscalar"), multi=False)

    variant("backend", default="CUDA", description="Accelerator backend", values=("CUDA", "ROCM"), multi=False)
    depends_on("qmp", when="parallel_arch=parscalar")

    variant("examples", default=False, description="Build Examples")
    variant("prop_opt", default=False, description="Enable Propagator Optimizations")
    variant("precision", default="double", description="QDP++ base precision", 
        values=("single", "double"), multi=False)

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        print("SPECK IS", self.spec)
        try:
            build_type = self.spec.variants["build_type"].value
        except KeyError:
            build_type = "RelWithDebInfo"

        args = [
            define("CMAKE_C_EXTENSIONS", "OFF"),
            define("CMAKE_BUILD_TYPE", build_type),
            define_from_variant("QDP_PRECISION", "precision"),
            define_from_variant("QDP_ENABLE_BACKEND", "backend"),
            define_from_variant("QDP_BUILD_EXAMPLES", "examples"),
            define_from_variant("QDP_PROP_OPT", "prop_opt"),
            define("BUILD_SHARED_LIBS", "ON"),
            define("QDP_ENABLE_LLVM15", "ON"),
            define_from_variant("QDP_PARALLEL_ARCH","parallel_arch")
        ]

        if "+rocm" in self.spec :
            args.append( define("QDP_ENABLE_BACKEND", "ROCM") )
            args.append( define_from_variant("GPU_TARGETS", "amdgpu_target"))
            args.append(self.define("HIP_CXX_COMPILER", self.compiler.cxx))

        if "+cuda" in self.spec :
            args.append( define("QDP_ENABLE_BACKEND", "CUDA") )
            args.append( define_from_fariant("GPU_TARGETS", "cuda_arch") )
        return args
