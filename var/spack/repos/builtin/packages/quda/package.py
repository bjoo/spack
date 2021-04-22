from spack import *


class Quda(CMakePackage,CudaPackage):
    """The QUDA Library for Lattie QCD on GPUs"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://lattice.github.io/quda"
    git      = "https://github.com/lattice/quda"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['bjoo']

    # Can add other version but am looking just to be in sync with 
    # Moderner CMake for now for Chroma Linkage
    version('feature/moderner-cmake', branch="feature/moderner-cmake")

    # Override cuda variant to have it enabled by default 
    variant('cuda', default=True, description="BUILD With CUDA")

    variant('cuda_arch', default='70', description="Supported CUDA Archs",
            values=('30', '32', '35', '37',
                    '50', '52', '53',
                    '60', '61', '62',
                    '70', '72', '75',
                    '80', '86' ), multi=True)

    # Variants (aka CMake options)
    variant('mpi', default=False, description="Build with MPI")
    variant('qmp', default=False, description="Build with QMP")
    variant('openmp', default=False, description="Enable Host OpenMP Use")

    # Fermion types
    variant('clover',            default=True,  description="Enable Clover")
    variant('clover_hasenbusch', default=False,  description="Enable Hasenbusch Clover")
    variant('dwf',               default=True,  description="Enable DWF")
    variant('ndeg_twm',          default=False, description="Enable Non-degenerate Twisted Mass")
    variant('staggered',         default=True,  description="Enable Staggered")
    variant('twm',               default=False, description="Enable Twisted Mass")
    variant('twm_clover',        default=False, description="Enable Twisted Clover")
    variant('wilson',            default=True,  description="Enable Wilson Fermions")
    variant('dynamic_clover',    default=False, description="Enable Dynamic Clover computations")

    # Gauge things
    variant('force_gauge',       default=True,  description="Enable Gauge Force for MILC")
    variant('force_hisq',        default=True,  description="Enable HISQ Force for MILC")
    variant('gauge_alg',         default=True,  description="Enable Gauge Algorithms")
    variant('gauge_tools',       default=False, description="Enable gauge Tools")

    # MG
    variant('multigrid',         default=True,  description="Enable Multigrid")

    # Interfaces
    variant('qdpjit',            default=False, description="Enable QDPJIT -- use quda_alloc from QDPJIT")
    variant('interface_qdpjit',  default=False, description="Enable QDPJIT Interface")
    variant('interface_milc',    default=True,  description="Enable MILC Interface")
    variant('interface_cps',     default=False, description="Enable CPS Interface")
    variant('interface_qdp',     default=True,  description="Enable QDP Interface")
    variant('interface_tifr',    default=False, description="Enable TIFR Interface")

    # Build optios and standards
    variant('sharedlib',         default=True,  description="Build Shared Libs")
    variant('build_all_tests',   default=True,  description="Build All Tests")
    variant('cxxstd',            default='14',  description="C++ standard to use",
            values=('14','17'), multi=False)
    variant('precision',         default='14',  description="QUDA_PRECISION for faster builds",
            values=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'), multi=False)
    
    variant('reconstruct',          default='7',   description="QUDA_RECONSTRUCT for faster builds",
            values=('1','2','3','4','5','6','7'), multi=False)

    variant('fast_compile_reduce', default=False, description="Enable fast compilation for reductions")
    variant('fast_compile_dslash', default=False, description="Enable fast compilation for Dslash")


    #Specialied Build-Type values
    variant('build_type', default='DEVEL', description="The QUDA Build Type -- these are custom",
            values=('DEVEL', 'STRICT', 'RELEASE', 'DEBUG', 'HOSTDEBUG', 'SANITIZE'), multi=False)


    #Dependencies
    depends_on('cuda', when="+cuda")
    depends_on('cmake@3.18.0:', type='build')    # Minimum Required CMake

    # This makes sure we have a supported cuda_arch: Currently up to Fermi
    unsupported_cuda_archs = [ 'none', '10', '11', '12', '13', '20', '21'   ]
    for value in unsupported_cuda_archs:
        conflicts('cuda_arch={0}'.format(value), when='+cuda',
                  msg='CUDA architecture {0} is not supported'.format(value))
    
    # MPI Dependency for MPI builds
    depends_on('mpi', when="+mpi")
    conflicts('+mpi', when='+qmp',
              msg='Cant have both QMP and MPI enabled')

    # QMP Dependency for QMP builds
    depends_on('qmp', when="+qmp")
    conflicts('+qmp', when='+mpi',
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
            self.define_from_variant('QUDA_DYNAMIC_CLOVER', 'dynamic_clover'),
            self.define_from_variant('QUDA_FORCE_GAUGE', 'force_gauge'),
            self.define_from_variant('QUDA_FORCE_HISQ', 'force_hisq'),
            self.define_from_variant('QUDA_GAUGE_ALG', 'gauge_alg'),
            self.define_from_variant('QUDA_GAUGE_TOOLS', 'gauge_tools'),
            self.define_from_variant('QUDA_QDPJIT', 'qdpjit'),
            self.define_from_variant('QUDA_INTERFACE_QDPJIT', 'interface_qdpjit'),
            self.define_from_variant('QUDA_INTERFACE_MILC',   'interface_milc'),
            self.define_from_variant('QUDA_INTERFACE_CPS',    'interface_cps'),
            self.define_from_variant('QUDA_INTERFACE_QDP',    'interface_qdp'),
            self.define_from_variant('QUDA_INTERFACE_TFIR',   'interface_tifr'),
            self.define_from_variant('QUDA_MULTIGRID', 'multigrid'),
            self.define_from_variant('QUDA_BUILD_SHAREDLIB', 'sharedlib'),
            self.define_from_variant('QUDA_BUILD_ALL_TESTS', 'build_all_tests'),
            self.define_from_variant('QUDA_FAST_COMPILE_REDCUCE', 'fast_compile_reduce'),
            self.define_from_variant('QUDA_FAST_COMPILE_DSLASH', 'fast_compile_dslash'),
            '-DCMAKE_CXX_STANDARD={0}'.format(spec.variants['cxxstd'].value),
            '-DQUDA_PRECISION={0}'.format(spec.variants['precision'].value),
            '-DQUDA_RECONSTRUCT={0}'.format(spec.variants['reconstruct'].value)
        ]

        if '+cuda' in spec:
            args.extend(['-DQUDA_TARGET_TYPE=CUDA' ])
            cuda_arch_list = spec.variants['cuda_arch'].value
            args.extend(['-DQUDA_GPU_ARCH=sm_{0}'.format(cuda_arch_list[0]) ])

        args.extend( [self.define_from_variant('-DQUDA_MPI', 'mpi')] )
        args.extend( [self.define_from_variant('-DQUDA_QMP', 'qmp')] )

        return args;
            
                    
        

    
