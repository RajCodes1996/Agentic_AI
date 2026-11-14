(venv) PS C:\Users\netware\Desktop\agentic_ai\Day-01-Research-Assistant> python -m pytest -v
=========================================================================================== test session starts ============================================================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\netware\Desktop\agentic_ai\Day-01-Research-Assistant\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\netware\Desktop\agentic_ai\Day-01-Research-Assistant
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.16.0
collected 9 items                                                                                                                                                                                           

tests/test_agent.py::test_successful_research PASSED                                                                                                                                                  [ 11%]
tests/test_agent.py::test_research_stops_without_evidence PASSED                                                                                                                                      [ 22%]
tests/test_agent.py::test_invalid_citation_detection PASSED                                                                                                                                           [ 33%]
tests/test_agent.py::test_empty_topic PASSED                                                                                                                                                          [ 44%]
tests/test_planner.py::test_create_research_plan PASSED                                                                                                                                               [ 55%]
tests/test_planner.py::test_empty_topic PASSED                                                                                                                                                        [ 66%]
tests/test_planner.py::test_whitespace_topic PASSED                                                                                                                                                   [ 77%]
tests/test_report_generator.py::test_generate_markdown_report PASSED                                                                                                                                  [ 88%]
tests/test_report_generator.py::test_save_report PASSED                                                                                                                                               [100%]

============================================================================================ 9 passed in 6.39s =============================================================================================
(venv) PS C:\Users\netware\Desktop\agentic_ai\Day-01-Research-Assistant> python -c "import agent, planner, report_generator; print('All imports successful')"
All imports successful
(venv) PS C:\Users\netware\Desktop\agentic_ai\Day-01-Research-Assistant> 