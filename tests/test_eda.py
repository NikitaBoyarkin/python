import pandas as pd
import pytest

from python_analytics.eda import correlation_matrix, describe, missing_report


def test_describe_has_mean_median_quantiles():
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0]})
    stats = describe(df)
    assert "mean" in stats.columns
    assert "median" in stats.columns
    assert "25%" in stats.columns
    assert stats.loc["a", "median"] == 2.5


def test_missing_report():
    df = pd.DataFrame({"a": [1, None, 3], "b": [1, 2, 3]})
    report = missing_report(df)
    assert list(report.index) == ["a"]
    assert report.loc["a", "missing"] == 1
    assert report.loc["a", "pct"] == round(1 / 3, 4)


def test_missing_report_empty_when_no_missing():
    df = pd.DataFrame({"a": [1, 2, 3]})
    assert missing_report(df).empty


def test_correlation_matrix_numeric_only():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [2, 4, 6], "c": ["x", "y", "z"]})
    corr = correlation_matrix(df)
    assert list(corr.columns) == ["a", "b"]
    assert corr.loc["a", "b"] == pytest.approx(1.0)
