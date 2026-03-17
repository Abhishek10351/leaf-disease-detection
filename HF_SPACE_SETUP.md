# Deploy To Hugging Face Spaces (via GitHub)

This repo can be deployed as a Docker Space directly from GitHub.

## 1. Push this repo to GitHub
Use your existing `main` branch or a dedicated `hf-space` branch.

## 2. Create a new Hugging Face Space
- Go to Hugging Face -> New Space
- SDK: `Docker`
- Visibility: your choice
- Choose `Import from GitHub`
- Select this repository and branch

## 3. Add Space secrets (Settings -> Variables and secrets)
Set these as **Secrets** (not plain variables):
- `OPENROUTER_API_KEY`

Set these as Variables (or Secrets):
- `MONGODB_URI`
- `MONGODB_DB_NAME`
- `OPENROUTER_SYNTHESIZER_MODEL` (optional override)
- `OPENROUTER_TEXT_MAX_TOKENS` (optional)
- `OPENROUTER_VISION_MAX_TOKENS` (optional)
- `OPENROUTER_GIST_MAX_TOKENS` (optional)
- `OPENROUTER_GIST_WORD_LIMIT` (optional)
- `BACKEND_CORS_ORIGINS` (set your frontend domain)
- `FRONTEND_HOST` (set your frontend domain)
- `ENVIRONMENT=production`

## 4. Build + run
Hugging Face will automatically build with root `Dockerfile` and run on `PORT=7860`.

## 5. Verify
Open your Space URL and check:
- `/docs`
- `/openapi.json`

## Notes
- `server/.env` is not used in production on Hugging Face; environment comes from Space secrets/variables.
- If you rotate model settings, trigger a Space restart/rebuild.
- If your frontend is hosted elsewhere (e.g. Vercel), set CORS values accordingly.
