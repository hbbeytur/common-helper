from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, TypedDict


class _LineSeries(TypedDict):
    kind: Literal["line"]
    label: str | None
    x: list[float]
    y: list[float]


class _ScatterSeries(TypedDict):
    kind: Literal["scatter"]
    label: str | None
    xy: list[tuple[float, float]]
    sizes: list[float] | None


class _BarSeries(TypedDict):
    kind: Literal["bar"]
    label: str | None
    x: list[float]
    height: list[float]
    width: list[float] | None
    bottom: list[float] | None


class _AxesPlotData(TypedDict):
    index: int
    title: str
    xlabel: str
    ylabel: str
    series: list[_LineSeries | _ScatterSeries | _BarSeries]


class FigurePlotData(TypedDict):
    axes: list[_AxesPlotData]


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


def extract_plot_data_points(fig: Any) -> FigurePlotData:
    """Extract plotted data points from a matplotlib figure.

    This walks the figure's Axes and extracts data from common plot types:
    - Lines (``ax.plot``): x/y values from ``Line2D`` artists
    - Scatter (``ax.scatter``): xy points (and sizes when available)
    - Bars (``ax.bar``): x centers and heights

    The output is intentionally a plain-Python structure (lists/dicts) so it can
    be JSON-serialized easily.

    Parameters
    ----------
    fig:
        A matplotlib ``Figure`` (typically ``matplotlib.figure.Figure``).

    Returns
    -------
    FigurePlotData
        Dictionary containing one entry per Axes with a list of extracted series.
    """

    def _is_matplotlib_type(obj: Any, *, class_name: str, module_prefix: str) -> bool:
        """Best-effort check without importing matplotlib types."""
        obj_type = type(obj)
        return obj_type.__name__ == class_name and obj_type.__module__.startswith(module_prefix)

    def _to_float_list(values: Any) -> list[float]:
        if values is None:
            return []
        # numpy arrays expose .tolist(); lists/tuples don't.
        if hasattr(values, "tolist"):
            values = values.tolist()
        return [float(v) for v in list(values)]

    def _clean_label(label: str | None) -> str | None:
        if label is None:
            return None
        # Matplotlib uses internal labels like '_child0' when none provided.
        return None if label.startswith("_") else label

    axes_data: list[_AxesPlotData] = []
    for ax_index, ax in enumerate(getattr(fig, "get_axes")()):
        series: list[_LineSeries | _ScatterSeries | _BarSeries] = []

        # Lines
        for line in ax.get_lines():
            x = _to_float_list(line.get_xdata())
            y = _to_float_list(line.get_ydata())
            series.append(
                {
                    "kind": "line",
                    "label": _clean_label(line.get_label()),
                    "x": x,
                    "y": y,
                }
            )

        # Scatter (PathCollection)
        for col in getattr(ax, "collections", []):
            if not _is_matplotlib_type(col, class_name="PathCollection", module_prefix="matplotlib."):
                continue
            offsets = col.get_offsets()
            if hasattr(offsets, "tolist"):
                offsets = offsets.tolist()
            xy = [(float(x), float(y)) for x, y in list(offsets)]
            sizes_raw = None
            if hasattr(col, "get_sizes"):
                sizes_raw = col.get_sizes()
            sizes = None
            if sizes_raw is not None:
                sizes = _to_float_list(sizes_raw)
            series.append(
                {
                    "kind": "scatter",
                    "label": _clean_label(getattr(col, "get_label", lambda: None)()),
                    "xy": xy,
                    "sizes": sizes,
                }
            )

        # Bars (BarContainer)
        for container in getattr(ax, "containers", []):
            if not _is_matplotlib_type(container, class_name="BarContainer", module_prefix="matplotlib."):
                continue
            x_centers: list[float] = []
            heights: list[float] = []
            widths: list[float] = []
            bottoms: list[float] = []
            for rect in container.patches:
                x_centers.append(float(rect.get_x() + rect.get_width() / 2.0))
                heights.append(float(rect.get_height()))
                widths.append(float(rect.get_width()))
                bottoms.append(float(rect.get_y()))
            series.append(
                {
                    "kind": "bar",
                    "label": _clean_label(getattr(container, "get_label", lambda: None)()),
                    "x": x_centers,
                    "height": heights,
                    "width": widths if widths else None,
                    "bottom": bottoms if bottoms else None,
                }
            )

        axes_data.append(
            {
                "index": ax_index,
                "title": ax.get_title(),
                "xlabel": ax.get_xlabel(),
                "ylabel": ax.get_ylabel(),
                "series": series,
            }
        )

    return {"axes": axes_data}
