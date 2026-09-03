import numpy as np
import pandas as pd
import pytest

from python_analytics.segment import (
    age_group,
    assign_age_group,
    group_summary,
    high_value_share,
    run_segmentation,
    segmentation_report,
    spend_rate,
    value_segments,
)


def _df():
    return pd.DataFrame(
        {
            "age": [22, 30, 45, 60, 70],
            "income": [40000, 50000, 60000, 70000, 80000],
            "spend": [10000.0, 20000.0, 30000.0, 40000.0, 50000.0],
        }
    )


def test_age_group_bounds():
    assert age_group(18) == "18-25"
    assert age_group(25) == "18-25"
    assert age_group(26) == "26-35"
    assert age_group(51) == "51-65"
    assert age_group(65) == "51-65"
    assert age_group(66) == "66+"
    assert age_group(17) == "other"


def test_assign_age_group():
    df = _df()
    result = assign_age_group(df)
    assert list(result) == ["18-25", "26-35", "36-50", "51-65", "66+"]


def test_spend_rate():
    df = _df()
    assert spend_rate(df).iloc[0] == 0.25
    assert spend_rate(df).iloc[-1] == 0.625


def test_spend_rate_zero_income_is_nan():
    df = pd.DataFrame({"spend": [10.0], "income": [0]})
    assert pd.isna(spend_rate(df).iloc[0])


def test_spend_rate_nan_income_is_nan():
    df = pd.DataFrame({"spend": [10.0], "income": [np.nan]})
    assert pd.isna(spend_rate(df).iloc[0])


def test_value_segments_four_buckets():
    df = _df()
    result = value_segments(df)
    assert result.dtype.name == "category"
    assert result.nunique() == 4
    assert set(result.cat.categories) == {"Low", "Medium-Low", "Medium-High", "High"}


def test_value_segments_nan_stays_nan():
    df = pd.DataFrame({"spend": [1.0, 2.0, 3.0, np.nan]})
    result = value_segments(df, n=2)
    assert pd.isna(result.iloc[-1])
    assert result.notna().sum() == 3


def test_value_segments_degenerate_does_not_raise():
    df = pd.DataFrame({"spend": [5.0, 5.0, 5.0, 5.0]})
    result = value_segments(df, n=4)
    assert result.nunique() == 1


def test_high_value_share_pareto():
    df = pd.DataFrame({"spend": [100.0, 1.0, 1.0, 1.0, 1.0]})
    assert high_value_share(df, top=0.2) == pytest.approx(100 / 104)


def test_high_value_share_zero_total():
    df = pd.DataFrame({"spend": [0.0, 0.0, 0.0]})
    assert high_value_share(df) == 0.0


def test_group_summary_counts_and_share():
    df = pd.DataFrame({"group": ["a", "a", "b"], "value": [1.0, 2.0, 3.0]})
    result = group_summary(df, "group", "value")
    assert result.loc["a", "count"] == 2
    assert result.loc["b", "count"] == 1
    assert result["share_of_total"].sum() == pytest.approx(1.0)
    assert np.isfinite(result["share_of_total"]).all()


def test_run_segmentation_returns_expected_keys():
    result = run_segmentation(_df())
    for key in ("enriched", "age_groups", "spend_rate_by_age", "value_segments", "pareto"):
        assert key in result
    assert len(result["age_groups"]) == 5
    assert 0.0 <= result["pareto"] <= 1.0


def test_run_segmentation_does_not_mutate_input():
    df = _df()
    original = df.copy()
    run_segmentation(df)
    pd.testing.assert_frame_equal(df, original)


def test_segmentation_report_writes_file(tmp_path):
    result = segmentation_report(_df(), str(tmp_path))
    assert (tmp_path / "segmentation_report.md").exists()
    assert "age_group" in result.columns
