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

## Install from a private GitHub repo

SSH:

```bash
pip install "common-helper @ git+ssh://git@github.com/<ORG_OR_USER>/<REPO>.git"
```

HTTPS (will prompt for credentials / token depending on your setup):

```bash
pip install "common-helper @ git+https://github.com/<ORG_OR_USER>/<REPO>.git"
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
