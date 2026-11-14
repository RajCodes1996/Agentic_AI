import pytest

from planner import create_research_plan

def test_create_research_plan():

    plan = create_research_plan("Generative AI")

    assert plan.topic == "Generative AI"

    assert len(plan.research_questions) > 0

    assert len(plan.expected_sections) > 0

def test_empty_topic():

    with pytest.raises(ValueError):
        create_research_plan("")

def test_whitespace_topic():

    with pytest.raises(ValueError):
        create_research_plan("   ")