
### Final architecture
PDF Intelligence Agent
End-to-end RAG architecture

PDF Upload

Streamlit interface · PDF validation

PDF Text Extraction

PyMuPDF · Preserve page numbers

Text Chunking

Meaningful text segments · Overlapping chunks

Embedding Generation

Sentence Transformers · Local embeddings

Vector Database

ChromaDB · Similarity search

Retriever

Find the most relevant document chunks

LLM Provider

(Ollama – Local) (Gemini – Cloud)

Grounded answer generation

Final Answer + Page Citations

Supporting excerpts · Streamlit chat interface
Technology decisions
Component	Technology
Programming	Python
Frontend	Streamlit
PDF extraction	PyMuPDF
Text chunking	Custom Python
Embeddings	Sentence Transformers
Embedding model	all-MiniLM-L6-v2
Vector database	ChromaDB
LLM 1	Ollama
LLM 2	Gemini
Configuration	python-dotenv
Data validation	Pydantic
Testing	Pytest

One important architectural decision: Embeddings will run locally, independently of the LLM. This means switching between Ollama and Gemini will not require reprocessing the PDF.
2. How the application will work
Imagine uploading a 100-page research paper and asking:

"What are the major limitations of the proposed methodology?"

Our application will:
1. Extract text from all 100 pages.
2. Break the extracted text into smaller chunks.
3. Convert each chunk into a numerical embedding.
4. Store those embeddings in ChromaDB.
5. Convert your question into an embedding.
6. Retrieve the most relevant chunks.
7. Send those chunks to the selected LLM.
8. Generate an answer with page references.
The LLM should answer using retrieved evidence, rather than pretending it has read information that wasn't retrieved.

Initial scope: Text-based PDFs, one document per session, local in-memory processing. OCR, multi-document collections and persistent document libraries can be future extensions.

### Our development roadmap
Here's how we'll build Agent 02:
Phase	Development milestone
01	Environment and project structure
02	PDF text extraction
03	Text chunking
04	Embedding generation
05	ChromaDB integration
06	Semantic retrieval
07	Ollama + Gemini integration
08	Complete RAG pipeline
09	Streamlit NEXUS UI
10	Testing, optimization and README
11	GitHub readiness