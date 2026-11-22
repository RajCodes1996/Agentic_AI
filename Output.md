(.venv) PS C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence> python -m pytest tests/test_vector_store.py -v
========================================================================================= test session starts =========================================================================================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence
plugins: anyio-4.16.0
collected 6 items                                                                                                                                                                                      

tests/test_vector_store.py::test_store_chunks PASSED                                                                                                                                             [ 16%]
tests/test_vector_store.py::test_store_metadata PASSED                                                                                                                                           [ 33%]
tests/test_vector_store.py::test_empty_chunks PASSED                                                                                                                                             [ 50%]
tests/test_vector_store.py::test_mismatched_embeddings PASSED                                                                                                                                    [ 66%]
tests/test_vector_store.py::test_duplicate_chunk_ids PASSED                                                                                                                                      [ 83%]
tests/test_vector_store.py::test_persistence PASSED                                                                                                                                              [100%]

========================================================================================= 6 passed in 20.21s ==========================================================================================