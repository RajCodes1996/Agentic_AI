
from planner import create_research_plan


topic = "Generative AI"

plan = create_research_plan(topic)

print("\nRESEARCH TOPIC:")
print(plan.topic)

print("\nRESEARCH QUESTIONS:")

for number, question in enumerate(
    plan.research_questions, start=1
):
    print(f"{number}. {question}")

print("\nEXPECTED REPORT SECTIONS:")

for section in plan.expected_sections:
    print("-", section)