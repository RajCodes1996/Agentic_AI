from types import SimpleNamespace

import pytest

import agent


def test_successful_research(monkeypatch):

    plan = SimpleNamespace(
        research_questions=[
            "What is Generative AI?"
        ]
    )

    evidence = [
        {
            "title": "Research Source",
            "url": "https://example.com",
            "research_question": "What is Generative AI?",
            "content": "Generative AI creates new content.",
            "score": 0.95
        }
    ]

    monkeypatch.setattr(
        agent,
        "create_research_plan",
        lambda topic: plan
    )

    monkeypatch.setattr(
        agent,
        "collect_research_evidence",
        lambda questions, results_per_question, max_workers=3: evidence
    )

    monkeypatch.setattr(
        agent,
        "generate_response",
        lambda prompt, provider: "Generative AI is useful [1]."
    )

    monkeypatch.setattr(
        agent,
        "generate_markdown_report",
        lambda topic, analysis, evidence: "# Test Report"
    )

    monkeypatch.setattr(
        agent,
        "save_report",
        lambda topic, report: "outputs/test.md"
    )

    result = agent.run_research(
        topic="Generative AI",
        provider="gemini"
    )

    assert result["analysis"] == "Generative AI is useful [1]."

    assert len(result["evidence"]) == 1

    assert result["saved_path"] == "outputs/test.md"

    assert result["invalid_citations"] == []


def test_research_stops_without_evidence(monkeypatch):

    plan = SimpleNamespace(
        research_questions=["What is Generative AI?"]
    )

    monkeypatch.setattr(
        agent,
        "create_research_plan",
        lambda topic: plan
    )

    monkeypatch.setattr(
        agent,
        "collect_research_evidence",
        lambda questions, results_per_question, max_workers=3: []
    )

    with pytest.raises(RuntimeError):
        agent.run_research(
            topic="Generative AI",
            provider="gemini"
        )


def test_invalid_citation_detection(monkeypatch):

    plan = SimpleNamespace(
        research_questions=["What is Generative AI?"]
    )

    evidence = [
        {
            "title": "Source 1",
            "url": "https://example.com",
            "research_question": "What is Generative AI?",
            "content": "Test evidence",
            "score": 0.9
        }
    ]

    monkeypatch.setattr(
        agent,
        "create_research_plan",
        lambda topic: plan
    )

    monkeypatch.setattr(
        agent,
        "collect_research_evidence",
        lambda questions, results_per_question, max_workers=3: evidence
    )

    monkeypatch.setattr(
        agent,
        "generate_response",
        lambda prompt, provider: "Finding A [1]. Finding B [5]."
    )

    monkeypatch.setattr(
        agent,
        "generate_markdown_report",
        lambda topic, analysis, evidence: "# Test Report"
    )

    monkeypatch.setattr(
        agent,
        "save_report",
        lambda topic, report: "outputs/test.md"
    )

    result = agent.run_research(
        topic="Generative AI",
        provider="gemini"
    )

    assert result["invalid_citations"] == [5]


def test_empty_topic():

    with pytest.raises(ValueError):
        agent.run_research(
            topic="   ",
            provider="gemini"
        )