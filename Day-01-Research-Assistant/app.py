import streamlit as st
from agent import run_research

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Research Assistant")

st.write(
    "An AI-powered research agent using web search "
    "and hybrid LLM providers."
)

provider = st.selectbox(
    "Select your AI provider",
    ["ollama", "gemini"]
)

topic = st.text_input(
    "Enter your research topic:"
)

if st.button("Start Research"):

    if not topic.strip():

        st.warning("Please enter a research topic.")

    else:

        try:

            with st.spinner("Your AI Research Agent is working..."):
                result = run_research(
                    topic=topic,
                    provider=provider
                )

            st.success("Research completed successfully!")

            # Research plan
            st.subheader("Research Plan")

            for question in result["plan"].research_questions:
                st.write(f"- {question}")

            # Collected sources
            st.subheader("Collected Research Sources")

            if not result["evidence"]:
                st.warning("No search results were returned.")
            else:
                for i, source in enumerate(
                    result["evidence"], start=1
                ):

                    with st.expander(
                        f"Source {i}: {source['title']}"
                    ):

                        st.write(source["content"])

                        st.write(
                            f"Relevance score: {source['score']}"
                        )

                        st.markdown(
                            f"[Open original source]({source['url']})"
                        )

            # Final analysis
            st.divider()

            st.subheader("Research Analysis")

            st.markdown(result["analysis"])

            # Performance Breakdown
            st.subheader("Performance Breakdown")
            for stage, duration in result["timings"].items():
                st.write(
                    f"**{stage.replace('_', ' ').title()}:** "
                    f"{duration} seconds"
                )
            total_time = sum(result["timings"].values())
            st.metric(
                "Total Processing Time",
                f"{total_time:.2f} seconds"
            )

            # Citation warning (if any)
            if result.get("invalid_citations"):
                st.warning(
                    "The report contains invalid citation "
                    f"numbers: {result['invalid_citations']}"
                )

            # Report download & file info
            st.download_button(
                label="Download Research Report",
                data=result["markdown_report"],
                file_name="research_report.md",
                mime="text/markdown"
            )

            st.caption(
                f"Report saved locally: {result['saved_path']}"
            )

        except Exception as error:

            st.error(
                f"Research process failed: {error}"
            )