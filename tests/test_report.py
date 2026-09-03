import pandas as pd

from python_analytics.report import generate_report


def test_generate_report_creates_markdown(tmp_path):
    df = pd.DataFrame({"age": [20, 30, 40, 50], "income": [100, 200, 300, 400]})
    path = generate_report(df, out_dir=str(tmp_path))
    assert path.exists()
    assert path.suffix == ".md"
    text = path.read_text(encoding="utf-8")
    assert "## Статистика" in text
    assert "## Корреляции" in text
    assert "![Гистограмма]" in text
    assert "![Тепловая карта]" in text
