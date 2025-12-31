import pytest


def test_pickle_roundtrip_and_modify(tmp_path):
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    from common_helper import load_figure_pickle, save_figure_pickle

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])

    pkl = tmp_path / "fig.pkl"
    save_figure_pickle(fig, pkl)

    loaded_fig = load_figure_pickle(pkl)

    # Modify after loading (the main goal)
    loaded_fig.suptitle("modified")

    out_png = tmp_path / "modified.png"
    loaded_fig.savefig(out_png)

    assert out_png.exists()
    assert out_png.stat().st_size > 0


def test_extract_plot_data_points_line_scatter_bar():
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    from common_helper import extract_plot_data_points

    fig, ax = plt.subplots()

    x_line = [0, 1, 2]
    y_line = [0, 1, 4]
    ax.plot(x_line, y_line, label="myline")

    xy_scatter = [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0)]
    ax.scatter([p[0] for p in xy_scatter], [p[1] for p in xy_scatter], s=[10, 20, 30])

    x_bar = [1, 2, 3]
    h_bar = [5, 6, 7]
    ax.bar(x_bar, h_bar, width=0.8)

    data = extract_plot_data_points(fig)
    assert "axes" in data
    assert len(data["axes"]) == 1

    series = data["axes"][0]["series"]
    kinds = [s["kind"] for s in series]
    assert "line" in kinds
    assert "scatter" in kinds
    assert "bar" in kinds

    line = next(s for s in series if s["kind"] == "line")
    assert line["x"] == [float(v) for v in x_line]
    assert line["y"] == [float(v) for v in y_line]
    assert line["label"] == "myline"

    scatter = next(s for s in series if s["kind"] == "scatter")
    assert scatter["xy"] == xy_scatter
    assert scatter["sizes"] == [10.0, 20.0, 30.0]

    bar = next(s for s in series if s["kind"] == "bar")
    assert bar["height"] == [float(v) for v in h_bar]
