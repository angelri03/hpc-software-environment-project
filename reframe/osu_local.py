"""OSU Micro-Benchmarks 7.5 -- local.

* ``fetch_osu_local``  -- downloads the tar once per session and verifies its SHA-256 checksum.
* ``build_osu_local``  -- compile-only test that builds the OSU Micro-Benchmarks from source.

run with:
reframe -c reframe/osu_local.py -n OSUBuildLocalCheck -r
"""

import os

import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.builtins import (fixture, run_after, run_before,
                                   sanity_function, variable)

OSU_VERSION = '7.5'
OSU_NAME = f'osu-micro-benchmarks-{OSU_VERSION}'
OSU_TAR = f'{OSU_NAME}.tar.gz'
OSU_URL = f'https://mvapich.cse.ohio-state.edu/download/mvapich/{OSU_TAR}'
OSU_SHA256 = '1cf84ac5419456202757a757c5f9a4f5c6ecd05c65783c7976421cfd6020b3b3'

OSU_PT2PT_DIR = os.path.join('c', 'mpi', 'pt2pt', 'standard')
OSU_BINARIES = ['osu_latency', 'osu_bw']


class fetch_osu_local(rfm.RunOnlyRegressionTest):
    descr = f'Fetch OSU Micro-Benchmarks {OSU_VERSION}'
    local = True
    sourcesdir = None
    executable = 'curl'
    executable_opts = ['-fsSLO', OSU_URL]
    postrun_cmds = [f'echo "{OSU_SHA256}  {OSU_TAR}" | sha256sum -c -']

    @sanity_function
    def validate_download(self):
        return sn.assert_found(rf'{OSU_TAR}: OK', self.stdout)


class build_osu_local(rfm.CompileOnlyRegressionTest):
    descr = f'Build OSU Micro-Benchmarks {OSU_VERSION} from source (foss/2025a)'
    build_system = 'Autotools'
    sourcesdir = None

    build_locally = False
    build_time_limit = '20m'
    build_cpus = variable(int, value=8)

    osu_bindir = variable(str)

    osu_source = fixture(fetch_osu_local, scope='session')

    @run_after('setup')
    def set_bindir(self):
        self.osu_bindir = os.path.join(self.stagedir, OSU_NAME, OSU_PT2PT_DIR)

    @run_before('compile')
    def prepare_build(self):
        tarball = os.path.join(self.osu_source.stagedir, OSU_TAR)
        self.prebuild_cmds = [f'tar xzf {tarball}', f'cd {OSU_NAME}']

        self.build_system.max_concurrency = self.build_cpus
        self.build_job.num_cpus_per_task = self.build_cpus

    @sanity_function
    def validate_build(self):
        return sn.all(
            sn.path_isfile(os.path.join(self.osu_bindir, exe))
            for exe in OSU_BINARIES
        )


@rfm.simple_test
class OSUBuildLocalCheck(build_osu_local):
    valid_systems = ['*']
    valid_prog_environs = ['foss-2025a']
    tags = {'osu', 'build', 'local'}
