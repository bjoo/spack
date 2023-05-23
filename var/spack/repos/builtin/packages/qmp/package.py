from spack import *


class Qmp(CMakePackage):
    """QMP Library"""

    homepage = "https://usqcd-software.github.io/qmp/"
    git      = "https://github.com/usqcd-software/qmp.git"

    maintainers = ['bjoo']

    # FIXME: Add proper versions and checksums here.
    version('master', branch='master')

    # This makes mpi building an option: +mpi
    variant('mpi', default=True, description="MPI Based build")
    depends_on('mpi', when="+mpi") 

    # Sanitizers
    variant('sanitizers', default=False, description="Build with Sanitizers enabled")
     


    depends_on('cmake@3.17.0:', type='build')
    def cmake_args(self):
        args = [ '-DCMAKE_C_STANDARD=99',
                 self.define_from_variant('QMP_MPI', 'mpi'),
                 self.define_from_variant('QMP_ENABLE_SANITIZERS', 'sanitizers') ]
        return args	


