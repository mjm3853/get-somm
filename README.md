# get-somm
AI Somm

## Project Structure

- `backend/` — LangGraph agent (backend), all backend code, configuration, and tests are self-contained here
- `frontend/` — Next.js UI frontend
- `.env` — Backend environment variables (Anthropic API key, etc.)
- `frontend/.env.local` — Frontend environment variables (see below)

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- Node.js (for UI)

## Setup

1. **Install Python dependencies:**

   ```bash
   uv sync
   ```

2. **Install UI dependencies:**

   ```bash
   cd frontend
   npm install
   # or yarn install, pnpm install, etc.
   ```

3. **Environment variables:**
   - Backend: Create a `.env` file in the root with your Anthropic API key and other secrets.
   - Frontend: Create a `frontend/.env.local` file with:
     ```env
     LANGCHAIN_API_KEY=your_langchain_api_key
     LANGGRAPH_API_URL=http://localhost:8123
     NEXT_PUBLIC_LANGGRAPH_ASSISTANT_ID=your_assistant_id_or_graph_id
     ```

## Running the Project (Development)

Open **two terminals**:

**Terminal 1: Start the LangGraph backend**

```bash
uv run langgraph dev
```

**Terminal 2: Start the UI**

```bash
cd frontend
npm run dev
```

- The backend will be available at [http://localhost:8123/docs](http://localhost:8123/docs)
- The UI will be available at [http://localhost:3000](http://localhost:3000)

## Deploy with Docker Compose

The backend and its dependencies (Redis, Postgres) can be run with Docker Compose:

```bash
uv run langgraph build
# Set IMAGE_NAME in .env
# Then:
docker-compose up
```

Navigate to [http://localhost:8123/docs](http://localhost:8123/docs) for backend API docs.

## Deep Eval Tests

```bash
uv run deepeval test run tests/deep_eval/test_cases.py
```

## TODO

- Try <https://github.com/Yonom/assistant-ui-langgraph-fastapi>
- Add Docker Compose support for the UI for a single-command workflow