SOFTWARE_SET = 'env/testing/2025a'
BATCH_OPTS = ['--partition=batch', '--qos=normal']


site_configuration = {
    'systems': [
        {
            'name': 'aion',
            'descr': 'ULHPC Aion - regular CPU nodes',
            'hostnames': [r'^aion'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'batch',
                    'descr': 'Aion regular CPU nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': BATCH_OPTS,
                    'modules': [SOFTWARE_SET],
                    'environs': ['builtin', 'foss-2025a', 'easybuild'],
                    'max_jobs': 8,
                    'time_limit': '10m',
                    'processor': {
                        'arch': 'zen2',
                        'num_cpus': 128,
                        'num_cpus_per_core': 1,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 64,
                    },
                },
            ],
        },
        {
            'name': 'iris',
            'descr': 'ULHPC Iris - regular CPU nodes (broadwell + skylake)',
            'hostnames': [r'^iris'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'broadwell',
                    'descr': 'Iris regular nodes (broadwell)',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': BATCH_OPTS + ['--constraint=broadwell'],
                    'modules': [SOFTWARE_SET],
                    'environs': ['builtin', 'foss-2025a', 'easybuild'],
                    'max_jobs': 8,
                    'time_limit': '10m',
                    'processor': {
                        'arch': 'broadwell',
                        'num_cpus': 28,
                        'num_cpus_per_core': 1,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 14,
                    },
                },
                {
                    'name': 'skylake',
                    'descr': 'Iris regular nodes (skylake)',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': BATCH_OPTS + ['--constraint=skylake'],
                    'modules': [SOFTWARE_SET],
                    'environs': ['builtin', 'foss-2025a', 'easybuild'],
                    'max_jobs': 8,
                    'time_limit': '10m',
                    'processor': {
                        'arch': 'skylake_avx512',
                        'num_cpus': 28,
                        'num_cpus_per_core': 1,
                        'num_sockets': 2,
                        'num_cpus_per_socket': 14,
                    },
                },
            ],
        },
    ],

    'environments': [
        {
            'name': 'foss-2025a',
            'modules': ['toolchain/foss/2025a'],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'ftn': 'mpifort',
            'target_systems': ['aion', 'iris'],
        },
        {
            'name': 'easybuild',
            'modules': ['tools/EasyBuild'],
            'target_systems': ['aion', 'iris'],
        },
    ],

    'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s',
                },
                {
                    'type': 'file',
                    'name': 'reframe.log',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: '
                              '%(check_info)s: %(message)s',
                    'append': False,
                },
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_display_name)s|%(check_system)s|'
                        '%(check_partition)s|%(check_environ)s|'
                        '%(check_jobid)s|%(check_job_nodelist)s|'
                        '%(check_result)s|%(check_perfvalues)s'
                    ),
                    'format_perfvars': (
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        '%(check_perf_unit)s|%(check_perf_ref)s|'
                        '%(check_perf_lower_thres)s|'
                        '%(check_perf_upper_thres)s|'
                    ),
                    'append': True,
                },
            ],
        },
    ],
}
