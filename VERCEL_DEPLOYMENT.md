# Deploy the ABC Assistant to Vercel with Docker

Vercel detects `Dockerfile.vercel` at the project root and deploys it as a container-backed Function. The regular `Dockerfile` provides the same application for local Docker use. Both run the FastAPI API in `main.py`.

## Services and configuration

Create a Pinecone project, a Groq API key, and a managed Redis instance. Redis stores chat history across container instances; the container must not run its own Redis server. Add these variables to the Vercel project's Production and Preview environments:

| Variable | Purpose |
| --- | --- |
| `PINECONE_API_KEY` | Access to Pinecone |
| `PINECONE_INDEX_NAME` | Name of the populated index |
| `PINECONE_CLOUD` | Cloud for index creation (default `aws`) |
| `PINECONE_REGION` | Region for index creation (default `us-east-1`) |
| `GROQ_API_KEY` | Access to Groq |
| `GROQ_MODEL` | Optional; defaults to `openai/gpt-oss-120b` |
| `REDIS_URL` | Managed Redis connection URL, preferably `rediss://...` |

The Vercel container sets `APP_ENV=production` and refuses to use process memory for chat history when `REDIS_URL` is missing. Do not commit real keys or your `.env` file.

## Ingest the knowledge base

Run ingestion once from your own machine or a separate job, before testing chat:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/ingest_data.py
```

Copy `.env.example` to `.env` and fill in Pinecone and Groq values first. The ingestion script creates the Pinecone index if it does not exist. The image intentionally does not ingest on startup: container instances may start repeatedly, and ingestion would duplicate records.

## Test the image locally

```powershell
docker build -t abc-assistant .
docker run --rm --env-file .env -p 8000:8000 abc-assistant
```

Open `http://localhost:8000/health`. Then test `POST /chat` with JSON such as:

```json
{"query":"What services does ABC offer?","session_id":"test-session"}
```

Without `REDIS_URL`, local Docker uses temporary in-process history for development.

## Deploy

Import the repository into a Vercel project or run `vercel` from this directory for a preview deployment, then `vercel --prod` for production. Select the container deployment if the dashboard asks for a framework preset. Vercel detects `Dockerfile.vercel`, builds the image, and routes HTTP traffic to it. Its container port defaults to 80; the command honors `PORT` if you set it in project settings.

After deployment, check `/health`, then `POST /chat` using an ABC-related question. `/health` confirms that the API started; it does not test Pinecone, Redis, or Groq. Review function logs if chat fails.

Vercel container deployments remain request-driven Functions with execution limits and no persistent local storage. Pinecone and Redis are external services. See [Vercel's container announcement](https://vercel.com/changelog/bring-your-dockerfile-to-vercel-functions) and [container port and storage guidance](https://vercel.com/i/can-you-run-docker-compose-on-vercel).
