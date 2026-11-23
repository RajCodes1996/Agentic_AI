(.venv) PS C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence> python -m pytest tests/test_rag_answer_service.py -v
============================================================================================ test session starts ============================================================================================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\.venv\Scripts\python.exe
cachedir: .pytest_cache                                                     
rootdir: C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence        
plugins: anyio-4.16.0     
collected 7 items                                                                                                                                                                                            

tests/test_rag_answer_service.py::test_generate_grounded_answer PASSED                                                                                                                                 [ 14%]
tests/test_rag_answer_service.py::test_page_numbers_are_in_prompt PASSED                                                                                                                               [ 28%]
tests/test_rag_answer_service.py::test_system_instruction_is_passed PASSED                                                                                                                             [ 42%]
tests/test_rag_answer_service.py::test_empty_question PASSED                                                                                                                                           [ 57%]
tests/test_rag_answer_service.py::test_invalid_top_k PASSED                                                                                                                                            [ 71%]
tests/test_rag_answer_service.py::test_no_retrieved_chunks PASSED                                                                                                                                      [ 85%]
tests/test_rag_answer_service.py::test_top_k_is_forwarded PASSED                                                                                                                                       [100%]

======================================================================================= 7 passed in 81.16s (0:01:21) ========================================================================================