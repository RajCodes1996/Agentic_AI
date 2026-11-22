platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence
plugins: anyio-4.16.0
collected 29 items                                                                                                                                                                          

tests/test_chunker.py::test_basic_chunking PASSED                                                                                                                                     [  3%]
tests/test_chunker.py::test_chunk_overlap PASSED                                                                                                                                      [  6%]
tests/test_chunker.py::test_page_number_preservation PASSED                                                                                                                           [ 10%]
tests/test_chunker.py::test_empty_pages PASSED                                                                                                                                        [ 13%]
tests/test_chunker.py::test_invalid_chunk_parameters PASSED                                                                                                                           [ 17%]
tests/test_chunker.py::test_natural_boundary_splitting PASSED                                                                                                                         [ 20%]
tests/test_embeddings.py::test_generate_embeddings PASSED                                                                                                                             [ 24%]
tests/test_embeddings.py::test_generate_query_embedding PASSED                                                                                                                        [ 27%]
tests/test_embeddings.py::test_empty_text_list PASSED                                                                                                                                 [ 31%]
tests/test_embeddings.py::test_invalid_document_text PASSED                                                                                                                           [ 34%]
tests/test_embeddings.py::test_empty_query PASSED                                                                                                                                     [ 37%]
tests/test_embeddings.py::test_embeddings_are_normalized PASSED                                                                                                                       [ 41%]
tests/test_pdf_extractor.py::test_pdf_text_extraction PASSED                                                                                                                          [ 44%]
tests/test_pdf_extractor.py::test_missing_pdf PASSED                                                                                                                                  [ 48%]
tests/test_pdf_extractor.py::test_invalid_file_extension PASSED                                                                                                                       [ 51%]
tests/test_pdf_extractor.py::test_empty_pdf PASSED                                                                                                                                    [ 55%]
tests/test_rag_pipeline.py::test_pipeline_indexes_and_answers PASSED                                                                                                                  [ 58%]
tests/test_retriever.py::test_retrieve_relevant_chunk PASSED                                                                                                                          [ 62%]
tests/test_retriever.py::test_top_k_limit PASSED                                                                                                                                      [ 65%]
tests/test_retriever.py::test_top_k_larger_than_collection PASSED                                                                                                                     [ 68%]
tests/test_retriever.py::test_empty_query PASSED                                                                                                                                      [ 72%]
tests/test_retriever.py::test_invalid_top_k PASSED                                                                                                                                    [ 75%]
tests/test_retriever.py::test_empty_collection PASSED                                                                                                                                 [ 79%]
tests/test_vector_store.py::test_store_chunks PASSED                                                                                                                                  [ 82%]
tests/test_vector_store.py::test_store_metadata PASSED                                                                                                                                [ 86%]
tests/test_vector_store.py::test_empty_chunks PASSED                                                                                                                                  [ 89%]
tests/test_vector_store.py::test_mismatched_embeddings PASSED                                                                                                                         [ 93%]
tests/test_vector_store.py::test_duplicate_chunk_ids PASSED                                                                                                                           [ 96%]
tests/test_vector_store.py::test_persistence PASSED                                                                                                                                   [100%]

===================================================================================== warnings summary =====================================================================================
.venv\Lib\site-packages\fitz\__init__.py:17
  C:\Users\netware\Desktop\agentic_ai\Day-02-PDF-Intelligence\.venv\Lib\site-packages\fitz\__init__.py:17: FutureWarning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
    warnings.warn(