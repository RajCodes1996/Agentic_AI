(.venv) PS C:\Users\netware\Desktop\agentic_ai> cd Day-02-PDF-Intelligenpython -c "import inspect, src.retrieval.retriever as r, src.pipeline.rag_answer_service as p; print('--- retriever ---'); print([n for n in dir(r) if not n.startswith('_')]); print('--- rag_answer_service ---'); print([n for n in dir(p) if not n.startswith('_')])"
--- retriever ---
['Retriever']
--- rag_answer_service ---
['RAGAnswerService']
(.venv) PS C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence> pytest -v
========================================================================================= test session starts =========================================================================================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence
plugins: anyio-4.16.0
collected 0 items / 9 errors                                                                                                                                                                           

=============================================================================================== ERRORS ================================================================================================
__________________________________________________________________________ ERROR collecting src/scripts/test_ollama_live.py ___________________________________________________________________________
ImportError while importing test module 'C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\src\scripts\test_ollama_live.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\scripts\test_ollama_live.py:4: in <module>
    from src.llm.ollama_provider import OllamaProvider
E   ModuleNotFoundError: No module named 'src'
_______________________________________________________________________________ ERROR collecting tests/test_chunker.py ________________________________________________________________________________
ImportError while importing test module 'C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\tests\test_chunker.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_chunker.py:4: in <module>
    from src.ingestion.chunker import TextChunker
E   ModuleNotFoundError: No module named 'src'
______________________________________________________________________________ ERROR collecting tests/test_embeddings.py ______________________________________________________________________________
ImportError while importing test module 'C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\tests\test_embeddings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_embeddings.py:5: in <module>
    from src.embeddings.embedding_service import EmbeddingService
E   ModuleNotFoundError: No module named 'src'
____________________________________________________________________________ ERROR collecting tests/test_llm_providers.py _____________________________________________________________________________
ImportError while importing test module 'C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\tests\test_llm_providers.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_llm_providers.py:6: in <module>
    from src.llm.ollama_provider import OllamaProvider
E   ModuleNotFoundError: No module named 'src'
____________________________________________________________________________ ERROR collecting tests/test_pdf_extractor.py _____________________________________________________________________________
ImportError while importing test module 'C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\tests\test_pdf_extractor.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_pdf_extractor.py:5: in <module>
    from src.ingestion.pdf_extractor import PDFExtractor
E   ModuleNotFoundError: No module named 'src'
__________________________________________________________________________ ERROR collecting tests/test_rag_answer_service.py __________________________________________________________________________
ImportError while importing test module 'C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\tests\test_rag_answer_service.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_rag_answer_service.py:4: in <module>
    from src.pipeline.rag_answer_service import RAGAnswerService
E   ModuleNotFoundError: No module named 'src'
_____________________________________________________________________________ ERROR collecting tests/test_rag_pipeline.py _____________________________________________________________________________
ImportError while importing test module 'C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\tests\test_rag_pipeline.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_rag_pipeline.py:1: in <module>
    from src.pipeline import RAGPipeline
E   ModuleNotFoundError: No module named 'src'
______________________________________________________________________________ ERROR collecting tests/test_retriever.py _______________________________________________________________________________
ImportError while importing test module 'C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\tests\test_retriever.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_retriever.py:5: in <module>
    from src.retrieval.retriever import Retriever
E   ModuleNotFoundError: No module named 'src'
_____________________________________________________________________________ ERROR collecting tests/test_vector_store.py _____________________________________________________________________________
ImportError while importing test module 'C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\tests\test_vector_store.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_vector_store.py:5: in <module>
    from src.retrieval.vector_store import VectorStore
E   ModuleNotFoundError: No module named 'src'
========================================================================================== warnings summary ===========================================================================================
.venv\Lib\site-packages\fitz\__init__.py:17
  C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\.venv\Lib\site-packages\fitz\__init__.py:17: FutureWarning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================================================================= short test summary info =======================================================================================
ERROR src/scripts/test_ollama_live.py
ERROR tests/test_chunker.py
ERROR tests/test_embeddings.py
ERROR tests/test_llm_providers.py
ERROR tests/test_pdf_extractor.py
ERROR tests/test_rag_answer_service.py
ERROR tests/test_rag_pipeline.py
ERROR tests/test_retriever.py
ERROR tests/test_vector_store.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 9 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
==================================================================================== 1 warning, 9 errors in 4.36s =====================================================================================