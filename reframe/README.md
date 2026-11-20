# HPC Software Environment — OSU Micro-Benchmarks

ReFrame tests for OSU Micro-Benchmarks (OMB) 7.5 on the ULHPC Aion and Iris clusters.

The **Existing Module** and **Generic Compilation** cases are implemented.

## Directory Structure

```text
project/
├── README.md
└── reframe/
    ├── config/
    │   ├── aion.py             # ReFrame configuration for Aion
    │   └── iris.py             # ReFrame configuration for Iris
    ├── scripts/
    │   └── prepare_omb.py      # Download, verify, cache, and extract OMB sources
    ├── osu_existing_module.py  # OMB tests using the existing module
    └── osu_generic_compile.py  # Build OMB from source and run benchmarks
```

## Usage

The tests use ReFrame and Slurm to run `osu_latency` and `osu_bw` with different MPI process placements.

Run the following commands from the corresponding cluster's login node.

First, enter the test directory from the repository root:

```bash
cd reframe
```

To run the reframe test scripts, we only need to load `devel/ReFrame` module.

**Aion:**

```bash
reframe -C config/aion.py -c osu_existing_module.py -r -v
```

**Iris:**

```bash
reframe -C config/iris.py -c osu_existing_module.py -r -v
```

To list the available tests without executing them, replace `-r -v` with `-l`.

To run the generic compilation tests, replace `osu_existing_module.py` with
`osu_generic_compile.py`. This case builds OMB 7.5 using `toolchain/foss/2025a`
and reuses the build for the latency and bandwidth tests. The source archive is
downloaded on cache misses, verified with SHA-256, and cached in `reframe/src/`.

ReFrame automatically handles Slurm job submission, CPU binding verification, benchmark execution, and performance extraction.

Test outputs are stored in the `output/` directories.

## Implementation Status

- **Existing Module:** Implemented and tested on Aion and Iris.
- **Generic Compilation:** On going.
- **EasyBuild Compilation:** Not implemented yet.

Iris does not support the same-socket, cross-NUMA test, so the corresponding cases are automatically skipped.
