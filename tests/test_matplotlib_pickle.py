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
