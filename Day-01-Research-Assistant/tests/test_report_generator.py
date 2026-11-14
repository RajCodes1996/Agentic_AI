from report_generator import (
    generate_markdown_report,
    save_report
)

def test_generate_markdown_report():

    topic = "Generative AI"

    analysis = "Generative AI has many applications."

    evidence = [
        {
            "title": "Research Source",
            "url": "https://example.com"
        }
    ]

    report = generate_markdown_report(
        topic,
        analysis,
        evidence
    )

    assert "# AI Research Report" in report
    assert topic in report
    assert analysis in report
    assert "https://example.com" in report

def test_save_report(tmp_path, monkeypatch):

    import report_generator

    monkeypatch.setattr(
        report_generator,
        "REPORT_DIR",
        tmp_path
    )

    report = "# Test Research Report"

    saved_path = save_report(
        "Generative AI",
        report
    )

    from pathlib import Path

    file_path = Path(saved_path)

    assert file_path.exists()

    assert file_path.read_text(
        encoding="utf-8"
    ) == report