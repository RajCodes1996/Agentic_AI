# Atlas PDF Intelligence

A compact Retrieval-Augmented Generation application for asking questions about uploaded PDFs.

## Run

```powershell
cd Day-02-PDF-Intelligence
py -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

Use **Ollama** with a locally running model, or set `GEMINI_API_KEY` and select Gemini. The app extracts text, chunks it, embeds the chunks, retrieves relevant context, and instructs the model to answer only from that context.

## Test

```powershell
py -m pytest -q
```
