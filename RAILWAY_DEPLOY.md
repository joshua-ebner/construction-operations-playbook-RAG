# Railway Deploy — Quick Steps (~15 min)

## 1. Push to GitHub

```bash
git init
git add .
git commit -m "Manufacturing supervisor RAG prototype"
git remote add origin <your-repo-url>
git push -u origin main
```

## 2. Create Railway project

1. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
2. Select this repo
3. Railway auto-detects Python via `requirements.txt`

## 3. Set environment variables

In Railway → Variables:

```
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```

For interview (Portkey):

```
USE_PORTKEY=true
PORTKEY_API_KEY=<provided>
PORTKEY_BASE_URL=https://portkeygateway.perficient.com/v1
LLM_MODEL=@aws-bedrock-use2/us.anthropic.claude-sonnet-4-5-20250929-v1:0
```

## 4. Start command

Already in `railway.toml`:

```
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

## 5. Generate public URL

Railway → Settings → Networking → Generate Domain

## 6. Smoke test deployed app

- Open URL, click an example question, confirm routing + answer
- First load may take 15–20s (Chroma index build)

## Notes

- `chroma_db/` is gitignored — index rebuilds on deploy (expected)
- Do NOT commit `.env`
