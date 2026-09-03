from python_analytics.pipeline import generate_synthetic_data, run_pipeline


def test_generate_synthetic_data_shape():
    df = generate_synthetic_data(n=100)
    assert len(df) >= 100  # +5 дубликатов
    assert {"age", "income", "spend"} <= set(df.columns)


def test_run_pipeline_end_to_end(tmp_path):
    result = run_pipeline(n=50, out_dir=str(tmp_path), data_dir=str(tmp_path))
    assert result["rows"] > 0
    assert result["hist"].endswith(".png")
    assert result["heatmap"].endswith(".png")
