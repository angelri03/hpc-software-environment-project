# HPC Software Environment Project

## Group Members

- Angelica Rings
- Hai Yu
- Poonam Sartale

## Repository Structure

| Folders       | Contents                                                 |
|---------------|----------------------------------------------------------|
| `reframe/`    | ReFrame tests, cluster configuration, and EasyConfig     |
| `results/`    | Results we chose to keep: perflogs, CSV tables, topology |
| `docs/`       | Documentation and CPU topology diagrams                  |

## Setup

Run on a cluster compute node, inside an interactive allocation:

```sh
salloc -p batch --qos=normal -N 1 -t 2:00:00
git clone https://github.com/angelri03/hpc-software-environment-project.git
cd hpc-software-environment-project
module load env/testing/2025a lang/Python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Tests

There is one ReFrame configuration per cluster, in `reframe/config/`. Run the tests from the `reframe/` folder with the configuration of the cluster you are on:

```sh
cd reframe

# aion
reframe -C config/aion.py -c osu_existing_module.py -r -v

# iris: pick the node type
reframe -C config/iris.py --system iris:broadwell -c osu_existing_module.py -r -v
reframe -C config/iris.py --system iris:skylake   -c osu_existing_module.py -r -v
```

See [reframe/README.md](reframe/README.md) for the full guide.
