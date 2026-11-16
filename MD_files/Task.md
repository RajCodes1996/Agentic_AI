The problem is in tests/test_agent.py, not in your actual concurrent-search implementation.
Fix these two mocks
1. In test_successful_research()

Find:
lambda questions, results_per_question: evidence



Replace with:
lambda questions, results_per_question, max_workers=3: evidence



2. In test_invalid_citation_detection()

Find:
lambda questions, results_per_question: evidence



Replace with:
lambda questions, results_per_question, max_workers=3: evidence



Your test_research_stops_without_evidence() is already passing, so leave it unchanged.