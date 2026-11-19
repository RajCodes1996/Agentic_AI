Day-02-PDF-Intelligence/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py
│   │   └── chunker.py
│   │
│   ├── embeddings/
│   │   ├── __init__.py
│   │   └── embedding_service.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── ollama_provider.py
│   │   └── gemini_provider.py
│   │
│   └── pipeline/
│       ├── __init__.py
│       └── rag_pipeline.py
│
├── tests/
│   ├── test_pdf_extractor.py
│   ├── test_chunker.py
│   ├── test_embeddings.py
│   ├── test_retriever.py
│   └── test_rag_pipeline.py
│
└── data/
    └── .gitkeep