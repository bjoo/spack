from spack import *


class Chroma(CMakePackage):
    """The Chroma Software System for Lattice QCD"""
    
    homepage = "https://jeffersonlab.github.io/chroma"
    git      = "https://github.com/jeffersonlab/chroma"

    # Package maintainers
    maintainers = ['bjoo']
    version('devel', branch='devel', submodules=True)

    # We can set this here -- and it will force the correct QDP++ dependency
    variant('parallel_arch', default='scalar', description="Set parallel arch for Chroma. Allowed values are scalar|parscalar",
            values=('scalar','parscalar'), multi=False)

    # Optional libs (included with chroma)
    variant('cpp_dslash', default=False, description="Set whether we want CPPWilsonDslash or not")
    variant('use_sse2', default=False, description="Set whether we want sse2 set or not")
    variant('use_sse3', default=False, description="Set whether we want sse3 set or not")
    variant('openmp', default=False, description="Set whether we want openmp or not")
    variant('sanitizers', default=False, description="Build with Sanitizers enabled")

    variant('qdpjit', default=False, description="Build with QDP-JIT");
    variant('jit_clover', default=False, description="Build with JIT Clover Term");
    variant('jit_clover', default=True, when="+qdpjit",  description="Build with JIT Clover Term");

    variant('quda', default=False, description="Build with QUDA");

    variant('lapack', default=False, description="Builds a lapack variant of the qdp-lapack submodule")
  
    depends_on("qdp-jit parallel_arch=parscalar", when="+qdpjit parallel_arch=parscalar")
    depends_on("qdp-jit parallel_arch=scalar", when="+qdpjit parallel_arch=scalar")
    depends_on("quda +qdpjit", when="+quda +qdpjit")

    depends_on("qdpxx parallel_arch=parscalar", when="~qdpjit parallel_arch=parscalar")
    depends_on("qdpxx parallel_arch=scalar", when="~qdpjit parallel_arch=scalar")
    depends_on("quda ~qdpjit", when="+quda ~qdpjit")
 
    depends_on('lapack', when='+lapack')
    
    depends_on('cmake@3.23.0:', type='build') # CMAKE_MINIMUM_VERSION
    

    def cmake_args(self):
        spec=self.spec
        args=[ self.define_from_variant('Chroma_ENABLE_CPP_WILSON_DSLASH', 'cpp_dslash'),
               self.define_from_variant('Chroma_ENABLE_SSE2', 'use_sse2'),
               self.define_from_variant('Chroma_ENABLE_SSE3', 'use_sse3'),
               self.define_from_variant('Chroma_ENABLE_OPENMP', 'openmp'),
               self.define_from_variant('Chroma_ENABLE_SANITIZERS', 'sanitizers'),
               self.define_from_variant('QDPLapack_ENABLE_SANITIZERS', 'sanitizers'),
               self.define_from_variant('Chroma_ENABLE_LAPACK', 'lapack')
        ]
        
        if "+cpp_dslash" in spec:
            dslash = [ self.define_from_variant('CPPWilsonDslash_ENABLE_SSE2', 'use_sse2'),
                       self.define_from_variant('CPPWilsonDslash_ENABLE_OPENMP', 'openmp'),
                       self.define_from_variant('CPPWilsonDslash_ENABLE_SANITIZERS', 'sanitizers') ]
            args = args + dslash

        if "+qdpjit" in spec:
            args.extend([ self.define_from_variant('Chroma_ENABLE_JIT_CLOVER', 'jit_clover') ])
        
        if "+quda" in spec:
            args.extend([ self.define_from_variant('Chroma_ENABLE_QUDA', 'quda')])


        return args

