### ISSUE (Needs to be fixed!)
- Application is taking long to hit the Api and generating very late and slow responses!
- UI needs to be updated

### 231 seconds (3 minutes 51 seconds) is far too slow for a research assistant. We should optimize this before calling Agent 01 production-ready.

However, I don't want to randomly change your code and potentially reduce research quality.
First, let's identify the bottleneck.
Your application has four timed stages:
Stage	What we're investigating
Planning	Research question generation
Web search	Tavily API response time
LLM analysis	Gemini/Ollama generation time
Report generation	Markdown creation and file saving

Please share these four timing values from your Streamlit output, along with which provider you selected (Gemini or Ollama).
What I suspect
The most likely bottlenecks are:
1. Sequential Tavily searches: Five research questions currently trigger five separate searches, one after another.
2. LLM processing: The model may be receiving too much source text.
3. Ollama inference: If the local model is running on CPU, generation can take considerably longer.
Our next optimization will focus on:
- Parallel Tavily searches using ThreadPoolExecutor.
- Limiting and cleaning retrieved evidence.
- Reducing unnecessary prompt tokens.
- Improving model selection and generation settings.
Target: Bring the research workflow down substantially from 231 seconds without sacrificing useful evidence or report quality.