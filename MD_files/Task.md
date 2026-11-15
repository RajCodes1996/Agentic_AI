
# TASK

Current execution sequence
1. Research planning
   Generate five research questions
2. Tavily search — Question 1
   Wait for search results
3. Tavily search — Question 2
   Wait for search results
4. Tavily search — Questions 3, 4 and 5
   Each search waits for the previous one
5. LLM analysis
   Send collected evidence to Gemini or Ollama
6. Report generation and saving
There are two different performance problems to distinguish:
- Web-search latency: multiple Tavily requests happen one after another.
- LLM latency: the model takes time to process the prompt and generate the report. Ollama may be slower on a CPU-powered machine.
Let's measure before changing the architecture.
Step 1. Measure exactly where the delay occurs
Open agent.py.
A. Add this import
from time import perf_counter


B. Inside run_research(), add timing around each stage
Replace the corresponding sections with these changes:

1. Research planning
timings = {}start = perf_counter()plan = create_research_plan(topic)timings["planning"] = round(    perf_counter() - start, 2)


2. Tavily evidence collection
start = perf_counter()evidence = collect_research_evidence(    plan.research_questions,    results_per_question=2)timings["web_search"] = round(    perf_counter() - start, 2)


Notice that I've reduced the results per question from 3 to 2. This is a small initial optimization.

3. LLM analysis
start = perf_counter()analysis = generate_response(    prompt=prompt,    provider=provider)timings["llm_analysis"] = round(    perf_counter() - start, 2)


Keep your existing empty-analysis validation immediately after this.

4. Report generation
start = perf_counter()markdown_report = generate_markdown_report(    topic=topic,    analysis=analysis,    evidence=evidence)saved_path = save_report(    topic=topic,    report=markdown_report)timings["report_generation"] = round(    perf_counter() - start, 2)


C. Return the timings
In the dictionary returned by run_research(), add:
"timings": timings


For example:
return {    "plan": plan,    "evidence": evidence,    "analysis": analysis,    "markdown_report": markdown_report,    "saved_path": saved_path,    "invalid_citations": invalid_citations,    "timings": timings}


Step 2. Display performance inside Streamlit
In app.py, after successful research, add:
st.subheader("Performance Breakdown")for stage, duration in result["timings"].items():    st.write(        f"**{stage.replace('_', ' ').title()}:** "        f"{duration} seconds"    )total_time = sum(result["timings"].values())st.metric(    "Total Processing Time",    f"{total_time:.2f} seconds")


Now your application will show exactly how much time each stage consumes.
Step 3. Three optimizations we'll apply
Component	Optimization	Expected benefit
Tavily	Reduce searches and run them concurrently	Less waiting for web results
LLM prompt	Limit unnecessary source text	Less input processing
Ollama	Use a suitable lightweight model	Faster local inference