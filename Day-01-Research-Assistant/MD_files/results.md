
tests/test_agent.py::test_successful_research FAILED                                    [ 11%]
tests/test_agent.py::test_research_stops_without_evidence PASSED                        [ 22%]
tests/test_agent.py::test_invalid_citation_detection FAILED                             [ 33%]
tests/test_agent.py::test_empty_topic PASSED                                            [ 44%]
tests/test_planner.py::test_create_research_plan PASSED                                 [ 55%]
tests/test_planner.py::test_empty_topic PASSED                                          [ 66%]
tests/test_planner.py::test_whitespace_topic PASSED                                     [ 77%]
tests/test_report_generator.py::test_generate_markdown_report PASSED                    [ 88%]
tests/test_report_generator.py::test_save_report PASSED                                 [100%]

========================================== FAILURES ==========================================
__________________________________ test_successful_research __________________________________

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x00000223381F29E0>

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
            lambda questions, results_per_question: evidence
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
    
>       result = agent.run_research(
            topic="Generative AI",
            provider="gemini"
        )

tests\test_agent.py:55: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

topic = 'Generative AI', provider = 'gemini', results_per_question = 2

    def run_research(
        topic: str,
        provider: str,
        results_per_question: int = 2
    ) -> dict:
    
        if not topic.strip():
            raise ValueError("Research topic cannot be empty.")
    
        timings = {}
    
        # STEP 1: Create research plan
        start = perf_counter()
        plan = create_research_plan(topic)
        timings["planning"] = round(perf_counter() - start, 2)
    
        # STEP 2: Collect web evidence
        start = perf_counter()
>       evidence = collect_research_evidence(
           plan.research_questions,
           results_per_question=2,
           max_workers=3
        )
E       TypeError: test_successful_research.<locals>.<lambda>() got an unexpected keyword argument 'max_workers'

agent.py:31: TypeError
______________________________ test_invalid_citation_detection _______________________________

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000002233812BD10>

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
            lambda questions, results_per_question: evidence
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
    
>       result = agent.run_research(
            topic="Generative AI",
            provider="gemini"
        )

tests\test_agent.py:138: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

topic = 'Generative AI', provider = 'gemini', results_per_question = 2

    def run_research(
        topic: str,
        provider: str,
        results_per_question: int = 2
    ) -> dict:
    
        if not topic.strip():
            raise ValueError("Research topic cannot be empty.")
    
        timings = {}
    
        # STEP 1: Create research plan
        start = perf_counter()
        plan = create_research_plan(topic)
        timings["planning"] = round(perf_counter() - start, 2)
    
        # STEP 2: Collect web evidence
        start = perf_counter()
>       evidence = collect_research_evidence(
           plan.research_questions,
           results_per_question=2,
           max_workers=3
        )
E       TypeError: test_invalid_citation_detection.<locals>.<lambda>() got an unexpected keyword argument 'max_workers'

agent.py:31: TypeError
================================== short test summary info ===================================
FAILED tests/test_agent.py::test_successful_research - TypeError: test_successful_research.<locals>.<lambda>() got an unexpected keyword argument...
FAILED tests/test_agent.py::test_invalid_citation_detection - TypeError: test_invalid_citation_detection.<locals>.<lambda>() got an unexpected keyword a...
================================ 2 failed, 7 passed in 4.65s =================================