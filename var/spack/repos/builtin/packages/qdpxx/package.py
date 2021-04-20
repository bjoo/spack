from spack import *


class Qdpxx(CMakePackage):
    """The QDP++ QCD Software Layer (CPU version)"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://usqcd-software.github.io/qdpxx"
    git     = "https://github.com/usqcd-software/qdpxx.git"

    # notify when the package is updated.
    maintainers = ['bjoo']

    
    # Add other versions here later
    version('devel', branch='devel', submodules=True)
    depends_on('libxml2')

    # Set QDP Parallel arch
    variant('parallel_arch', default='scalar', description="QDPXX Parallel arch: allowed values are scalar|parscalar",
            values=('scalar','parscalar'), multi=False)

    # Future variants: SSE/OpenMP?
    
    # Conditional dependency on QMP for parscalar builds
    # Can add also one for parscalarvec later
    depends_on('qmp', when="parallel_arch=parscalar")

    # CMake Minimum version
    depends_on('cmake@3.17.0:', type='build')

    # Sanitizers
    variant('sanitizers', default=False, description="Build with Sanitizers enabled")
    
    # Main flags just now
    def cmake_args(self):
        spec = self.spec
        args = [  self.define_from_variant('QDP_ENABLE_SANITIZERS', 'sanitizers') ]
        if "parallel_arch=parscalar" in spec:
            args.extend(["-DQDP_PARALLEL_ARCH=parscalar"])
        elif "parallel_arch=scalar" in spec:
            args.extend(["-DQDP_PARALLEL_ARCH=scalar"])

        return args
    



