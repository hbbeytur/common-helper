from __future__ import annotations

from pathlib import Path
from typing import Any


def save_figure_pickle(
    fig: Any,
    path: str | Path,
    *,
    protocol: int | None = None,
    mkdir: bool = True,
) -> Path:
    """Save a matplotlib figure to disk using pickle.

    This is intended for workflows where you want to load a figure later and
    keep modifying it (axes, labels, data, etc.).

    Notes
    -----
    - Security: never unpickle files from untrusted sources.
    - Compatibility: pickled figures may not load across different matplotlib
      versions or Python versions.

    Parameters
    ----------
    fig:
        A matplotlib ``Figure`` (or any pickle-able object).
    path:
        Output ``.pkl`` path.
    protocol:
        Pickle protocol. Defaults to ``pickle.HIGHEST_PROTOCOL``.
    mkdir:
        If True, create parent directories.

    Returns
    -------
    Path
        The written path.
    """

    import pickle

    out_path = Path(path).expanduser()
    if mkdir:
        out_path.parent.mkdir(parents=True, exist_ok=True)

    if protocol is None:
        protocol = pickle.HIGHEST_PROTOCOL

    with out_path.open("wb") as f:
        pickle.dump(fig, f, protocol=protocol)

    return out_path


def load_figure_pickle(path: str | Path) -> Any:
    """Load a matplotlib figure saved with :func:`save_figure_pickle`.

    Security warning: never unpickle files from untrusted sources.

    Returns
    -------
    Any
        Typically a matplotlib ``Figure``.
    """

    import pickle

    in_path = Path(path).expanduser()
    with in_path.open("rb") as f:
        return pickle.load(f)
