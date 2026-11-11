
from pydantic import BaseModel, Field
from typing import List


class ResearchPlan(BaseModel):
    topic: str

    research_questions: List[str] = Field(
        description="Smaller questions that need investigation"
    )

    expected_sections: List[str] = Field(
        description="Sections required in the final research report"
    )


def create_research_plan(topic: str) -> ResearchPlan:

    if not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    questions = [
        f"What is {topic}?",
        f"What are the latest developments in {topic}?",
        f"What are the practical applications of {topic}?",
        f"What are the advantages and limitations of {topic}?",
        f"What is the future scope of {topic}?"
    ]

    sections = [
        "Introduction",
        "Latest Developments",
        "Applications",
        "Advantages and Limitations",
        "Future Scope",
        "Conclusion"
    ]

    return ResearchPlan(
        topic=topic,
        research_questions=questions,
        expected_sections=sections
    )
