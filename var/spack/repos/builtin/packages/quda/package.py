from spack import *


class Quda(CMakePackage,CudaPackage,ROCmPackage):
    """The QUDA Library for Lattie QCD on GPUs"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://lattice.github.io/quda"
    git      = "https://github.com/bjoo/quda"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['bjoo']

    # Can add other version but am looking just to be in sync with 
    # Moderner CMake for now for Chroma Linkage
    version("develop", branch="develop")

    depends_on("git")

    # Variants (aka CMake options)
    variant("mpi_comms", default=False, description="Build with MPI")
    variant("qmp_comms", default=False, description="Build with QMP")
    variant("openmp", default=False, description="Enable Host OpenMP Use")

    # Fermion types
    variant("clover",            default=True,  description="Enable Clover")
    variant("clover_hasenbusch", default=False,  description="Enable Hasenbusch Clover")
    variant("dwf",               default=True,  description="Enable DWF")
    variant("ndeg_twm",          default=False, description="Enable Non-degenerate Twisted Mass")
    variant("staggered",         default=True,  description="Enable Staggered")
    variant("twm",               default=False, description="Enable Twisted Mass")
    variant("twm_clover",        default=False, description="Enable Twisted Clover")
    variant("wilson",            default=True,  description="Enable Wilson Fermions")
    variant("dynamic_clover",    default=True, description="Enable Dynamic Clover computations")

    # Gauge things
    variant('force_gauge',       default=True,  description="Enable Gauge Force for MILC")
    variant('force_hisq',        default=True,  description="Enable HISQ Force for MILC")
    variant('gauge_alg',         default=True,  description="Enable Gauge Algorithms")
    variant('gauge_tools',       default=False, description="Enable gauge Tools")

    # MG
    variant("multigrid",         default=True,  description="Enable Multigrid")

    # Interfaces
    variant("qdpjit",            default=False, description="Enable QDPJIT -- use quda_alloc from QDPJIT")
    variant("interface_milc",    default=True,  description="Enable MILC Interface")
    variant("interface_cps",     default=False, description="Enable CPS Interface")
    variant("interface_qdp",     default=True,  description="Enable QDP Interface")
    variant("interface_tifr",    default=False, description="Enable TIFR Interface")

    # Build optios and standards
    variant("sharedlib",         default=True,  description="Build Shared Libs")
    variant("build_all_tests",   default=True,  description="Build All Tests")
    variant("cxxstd",            default='14',  description="C++ standard to use",
            values=('14','17'), multi=False)
    variant("precision",         default='14',  description="QUDA_PRECISION for faster builds",
            values=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'), multi=False)
    
    variant("reconstruct",          default='7',   description="QUDA_RECONSTRUCT for faster builds",
            values=('1','2','3','4','5','6','7'), multi=False)

    variant('fast_compile_reduce', default=False, description="Enable fast compilation for reductions")
    variant('fast_compile_dslash', default=False, description="Enable fast compilation for Dslash")


    #Specialied Build-Type values
    variant("build_type", default="DEVEL", description="The QUDA Build Type -- these are custom",
            values=("DEVEL", "STRICT", "RELEASE", "DEBUG", "HOSTDEBUG", "SANITIZE"), multi=False)

    variant('quda_max_multiblas', default="9", description="Multi Blas N")

    # MDW fused LS LIST
    #variant("mdw_fused_ls_list", default="4,8,12,16,20", description="MDWF Fused Ls List",
    #        values=("4","8","12","16","20"), multi=True)

    #variant("mg_nvec_list", default="6,24,32", description="Multigrid NVec List",
    #        values=("6","24","32","48","64","96"), multi=True)
    
    #Dependencies
    depends_on("cuda", when="+cuda")
    depends_on("qdp-jit", when="+qdpjit")
    depends_on("mpi", when="+qdpjit")
    depends_on("cmake@3.23.0:", type="build")    # Minimum Required CMake

    variant("cray", default=False, description="Set to +cray to use Cray Wrappers")
    # This makes sure we have a supported cuda_arch: Currently up to Fermi
    
    # MPI Dependency for MPI builds
    depends_on("mpi", when="+mpi_comms")
    conflicts("+mpi_comms", when="+qmp_comms",
              msg='Cant have both QMP and MPI enabled')

    # QMP Dependency for QMP builds
    depends_on("qmp", when="+qmp_comms")
    conflicts('+qmp_comms', when='+mpi_comms',
              msg='Cant have both QMP and MPI enabled')
   
    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant('QUDA_DIRAC_CLOVER', 'clover'),
            self.define_from_variant('QUDA_DIRAC_CLOVER_HASENBUSCH', 'clover_hasenbusch'),
            self.define_from_variant('QUDA_DIRAC_DOMAIN_WALL', 'dwf'),
            self.define_from_variant('QUDA_DIRAC_NDEG_TWISTED_MASS','ndeg_twm'),
            self.define_from_variant('QUDA_DIRAC_STAGGERED','staggered'),
            self.define_from_variant('QUDA_DIRAC_TWISTED_MASS', 'twm'),
            self.define_from_variant('QUDA_DIRAC_TWISTED_CLOVER', 'twm_clover'),
            self.define_from_variant('QUDA_DIRAC_WILSON', 'wilson'),
            self.define_from_variant('QUDA_CLOVER_DYNAMIC', 'dynamic_clover'),
            self.define_from_variant('QUDA_QDPJIT', 'qdpjit'),
            self.define_from_variant('QUDA_INTERFACE_QDPJIT', 'qdpjit'),
            self.define_from_variant('QUDA_INTERFACE_MILC',   'interface_milc'),
            self.define_from_variant('QUDA_INTERFACE_CPS',    'interface_cps'),
            self.define_from_variant('QUDA_INTERFACE_QDP',    'interface_qdp'),
            self.define_from_variant('QUDA_INTERFACE_TIFR',   'interface_tifr'),
            self.define_from_variant('QUDA_MULTIGRID', 'multigrid'),
            self.define_from_variant('QUDA_MAX_MULTI_BLAS_N', 'quda_max_multiblas'),
            self.define_from_variant('QUDA_BUILD_SHAREDLIB', 'sharedlib'),
            self.define_from_variant('QUDA_BUILD_ALL_TESTS', 'build_all_tests'),
            self.define_from_variant('QUDA_INSTALL_ALL_TESTS', 'build_all_tests'),
            self.define_from_variant('QUDA_FAST_COMPILE_REDUCE', 'fast_compile_reduce'),
            self.define_from_variant('QUDA_FAST_COMPILE_DSLASH', 'fast_compile_dslash'),
            self.define('QUDA_EIGEN_VERSION', "3.3.9"),
            '-DCMAKE_CXX_STANDARD={0}'.format(spec.variants['cxxstd'].value),
            '-DQUDA_PRECISION={0}'.format(spec.variants['precision'].value),
            '-DQUDA_RECONSTRUCT={0}'.format(spec.variants['reconstruct'].value),
            self.define('QUDA_SPACK_BUILD', 'ON')
        ]

        if '+cuda' in spec:
            args.extend(['-DQUDA_TARGET_TYPE=CUDA' ])
            cuda_arch_list = spec.variants['cuda_arch'].value
            args.extend(['-DQUDA_GPU_ARCH=sm_{0}'.format(cuda_arch_list[0]) ])

        if '+rocm' in spec:
            args.extend(['-DQUDA_TARGET_TYPE=HIP' ])
            args.extend([ self.define_from_variant('QUDA_GPU_ARCH', "amdgpu_target") ])
            args.append(self.define("HIP_CXX_COMPILER", self.compiler.cxx))
 
        if '+qdpjit' in spec:
            args.extend([self.define_from_variant('QUDA_QMP', 'qdpjit')])

        if '+qmp_comms' in spec:
            args.extend([self.define_from_variant('QUDA_QMP', 'qmp_comms')])
        
        if '+mpi_comms' in spec:
            args.extend([self.define_from_variant('QUDA_MPI', 'mpi_comms')])

        return args;
