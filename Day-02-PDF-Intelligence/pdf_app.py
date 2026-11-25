import hashlib
import os
import tempfile
from pathlib import Path

import streamlit as st

from config import settings
from src.ingestion.pdf_extractor import PDFExtractor
from src.llm import OllamaProvider
from src.pipeline import RAGPipeline


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="PDF Intelligence Agent",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF Intelligence Agent")
st.caption(
    "Upload a PDF, understand its contents, "
    "and ask questions using Retrieval-Augmented Generation."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "pipeline": None,
    "document_name": None,
    "document_hash": None,
    "messages": [],
    "uploader_key": 0,
    "indexed_chunks": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("Settings")

    ollama_model = st.text_input(
        "Ollama model",
        value=os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")
    )

    st.divider()

    st.subheader("Document settings")

    st.write(f"Chunk size: {settings.chunk_size}")
    st.write(f"Chunk overlap: {settings.chunk_overlap}")

    st.divider()

    if st.button("🗑️ Clear document", use_container_width=True):

        st.session_state.pipeline = None
        st.session_state.document_name = None
        st.session_state.document_hash = None
        st.session_state.messages = []
        st.session_state.indexed_chunks = 0

        # Reset the uploader widget as well.
        st.session_state.uploader_key += 1

        st.rerun()


# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

st.header("1. Upload your PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"],
    key=f"pdf_upload_{st.session_state.uploader_key}"
)


# --------------------------------------------------
# PDF EXTRACTION AND INDEXING
# --------------------------------------------------

if uploaded_file is not None:

    pdf_bytes = uploaded_file.getvalue()
    current_hash = hashlib.sha256(pdf_bytes).hexdigest()

    if current_hash != st.session_state.document_hash:

        try:

            with st.spinner(
                "Extracting PDF text and creating vector embeddings..."
            ):

                # Save the uploaded PDF temporarily.
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf",
                    delete=False
                ) as temp_file:

                    temp_file.write(pdf_bytes)
                    temp_path = Path(temp_file.name)

                try:
                    pages = PDFExtractor().extract_text(temp_path)

                finally:
                    temp_path.unlink(missing_ok=True)

                # Create the RAG pipeline.
                llm = OllamaProvider(
                    model_name=ollama_model
                )

                pipeline = RAGPipeline(
                    llm=llm,
                    chunk_size=settings.chunk_size,
                    chunk_overlap=settings.chunk_overlap,
                    persist_directory="data/chroma_pdf_agent",
                    collection_name="pdf_agent_ui_384"
                )

                # Index page-wise content.
                chunk_count = pipeline.index(
                    pages,
                    source_name=uploaded_file.name
                )

                if chunk_count == 0:
                    raise ValueError(
                        "No text chunks could be created from this PDF."
                    )

                st.session_state.pipeline = pipeline
                st.session_state.document_name = uploaded_file.name
                st.session_state.document_hash = current_hash
                st.session_state.indexed_chunks = chunk_count
                st.session_state.messages = []

            st.success(
                f"Successfully indexed {chunk_count} chunks!"
            )

        except Exception as exc:

            st.error(f"PDF processing failed: {exc}")


# --------------------------------------------------
# DOCUMENT STATUS
# --------------------------------------------------

if st.session_state.pipeline is not None:

    st.divider()

    st.header("2. Document information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Indexed chunks",
            st.session_state.indexed_chunks
        )

    with col2:
        st.metric(
            "Document pages extracted",
            "Available in source evidence"
        )

    st.info(
        f"Current document: {st.session_state.document_name}"
    )


# --------------------------------------------------
# CHAT INTERFACE
# --------------------------------------------------

if st.session_state.pipeline is not None:

    st.divider()

    st.header("3. Ask questions about your PDF")

    # Display previous conversation.
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                sources = message.get("sources", [])

                if sources:

                    with st.expander(
                        f"📚 View retrieved evidence ({len(sources)} sources)"
                    ):

                        for index, source in enumerate(
                            sources,
                            start=1
                        ):

                            page = source.get("page_number", "Unknown")
                            chunk = source.get("chunk_id", "Unknown")
                            distance = source.get("distance")

                            st.markdown(
                                f"**Source {index} — Page {page} "
                                f"— Chunk {chunk}**"
                            )

                            if distance is not None:
                                st.caption(
                                    f"Cosine distance: {distance:.4f} "
                                    "(lower generally means more similar)"
                                )

                            st.write(source.get("text", ""))

                            st.divider()

    # New question input.
    question = st.chat_input(
        "Ask something about your uploaded PDF..."
    )

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        try:

            with st.chat_message("assistant"):

                with st.spinner(
                    "Searching the document and generating an answer..."
                ):

                    # Use the currently selected Ollama model.
                    st.session_state.pipeline.llm = OllamaProvider(
                        model_name=ollama_model
                    )

                    answer, sources = (
                        st.session_state.pipeline.answer(
                            question,
                            k=4
                        )
                    )

                st.markdown(answer)

                if sources:

                    with st.expander(
                        f"📚 View retrieved evidence ({len(sources)} sources)",
                        expanded=True
                    ):

                        for index, source in enumerate(
                            sources,
                            start=1
                        ):

                            page = source.get("page_number", "Unknown")
                            chunk = source.get("chunk_id", "Unknown")
                            distance = source.get("distance")

                            st.markdown(
                                f"**Source {index} — Page {page} "
                                f"— Chunk {chunk}**"
                            )

                            if distance is not None:
                                st.caption(
                                    f"Cosine distance: {distance:.4f}"
                                )

                            st.write(source.get("text", ""))

                            st.divider()

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

        except Exception as exc:

            st.error(f"Answer generation failed: {exc}")

else:

    st.info(
        "Upload a PDF document above to start asking questions."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "PDF Intelligence Agent | Local embeddings | "
    "ChromaDB | Ollama | Retrieval-Augmented Generation"
)