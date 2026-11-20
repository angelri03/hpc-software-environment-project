# HPC Software Environment Project

## Group Members

Angelica Rings
Hai Yu
Poonam Sartale

## Setup

One-time setup:

```sh
module load env/testing/2025a lang/Python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## ReFrame config

```sh
export RFM_CONFIG_FILES=$PWD/config/ulhpc.py
reframe --system aion --show-config
```
