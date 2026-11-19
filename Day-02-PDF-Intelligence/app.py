import streamlit as st
from config import settings
from src.ingestion import extract_pdf_text
from src.llm import GeminiProvider, OllamaProvider
from src.pipeline import RAGPipeline

st.set_page_config(page_title="Atlas PDF Intelligence", page_icon="📄", layout="wide")
st.title("Atlas · PDF Intelligence")
st.caption("Upload a PDF, index it locally, and ask grounded questions about its contents.")
with st.sidebar:
    provider = st.selectbox("Inference provider", ["Ollama", "Gemini"])
    st.caption("Embeddings run locally when sentence-transformers is installed.")
    if st.button("Clear document"):
        st.session_state.pop("pipeline", None); st.session_state.pop("document_name", None); st.rerun()

uploaded = st.file_uploader("PDF document", type="pdf")
if uploaded and (st.session_state.get("document_name") != uploaded.name):
    try:
        with st.spinner("Extracting and indexing document..."):
            text = extract_pdf_text(uploaded)
            llm = OllamaProvider(settings.ollama_model) if provider == "Ollama" else GeminiProvider(settings.gemini_api_key, settings.gemini_model)
            pipeline = RAGPipeline(llm, chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
            count = pipeline.index(text, uploaded.name)
            st.session_state.pipeline, st.session_state.document_name = pipeline, uploaded.name
        st.success(f"Indexed {count} chunks from {uploaded.name}.")
    except Exception as exc:
        st.error(str(exc))

if pipeline := st.session_state.get("pipeline"):
    question = st.chat_input("Ask a question about this PDF")
    if question:
        with st.chat_message("user"): st.write(question)
        try:
            with st.chat_message("assistant"):
                with st.spinner("Retrieving evidence and generating an answer..."):
                    answer, sources = pipeline.answer(question)
                st.write(answer)
                with st.expander("Retrieved evidence"):
                    for source in sources:
                        st.caption(f"Chunk {source['metadata']['chunk']} · relevance {source['score']:.2f}")
                        st.write(source["text"])
        except Exception as exc:
            st.error(str(exc))
