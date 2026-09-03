import pandas as pd

from python_analytics.viz import plot_corr_heatmap, plot_hist


def test_plot_hist_saves_png(tmp_path):
    df = pd.DataFrame({"age": [20, 30, 40, 50]})
    path = plot_hist(df, "age", tmp_path)
    assert path.exists()
    assert path.suffix == ".png"


def test_plot_corr_heatmap_saves_png(tmp_path):
    df = pd.DataFrame({"a": [1, 2, 3], "b": [2, 4, 6]})
    path = plot_corr_heatmap(df, tmp_path)
    assert path.exists()
    assert path.suffix == ".png"
