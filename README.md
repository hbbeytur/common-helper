# common_helper

Common helper utilities.

## Install into any virtual environment

You install a package **into the Python environment that runs `pip`**.

- Activating a venv (`source .venv/bin/activate`) is just a convenience so `python`/`pip` point to that venv.
- If you prefer not to “activate”, use the venv’s Python explicitly.

Example (recommended):

```bash
python -m venv .venv
./.venv/bin/python -m pip install -U pip
./.venv/bin/python -m pip install -e .
```

In a future venv you create, run the same pattern (replace the venv path).

## Install (local development)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e .
```

## Install with matplotlib support

```bash
pip install -e ".[plotting]"
```

## Install from GitHub

HTTPS:

```bash
pip install "common-helper @ git+https://github.com/hbbeytur/common-helper.git"
```

Optional extra (matplotlib):

```bash
pip install "common-helper[plotting] @ git+https://github.com/hbbeytur/common-helper.git"
```

## Usage

```py
from common_helper import save_figure_pickle, load_figure_pickle
```

## Test

```bash
pip install -U pytest
pytest
```
