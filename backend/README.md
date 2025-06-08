# get-somm Backend

This is the backend Python project for get-somm. All backend code, configuration, and tests are self-contained in this directory.

## Setup

1. **Install dependencies** (requires Python 3.11+ and [uv](https://github.com/astral-sh/uv)):
   ```sh
   uv sync
   ```

2. **Set up environment variables**:
   - Copy `.env.example` to `.env` and fill in required values (if `.env.example` exists), or create a `.env` file with the necessary secrets (e.g., Anthropic API key).

## Running

- **Start the backend in development mode:**
  ```sh
  uv run langgraph dev
  ```

- **Run tests:**
  ```sh
  uv run pytest
  ```

- **Build Docker image:**
  ```sh
  uv run langgraph build
  ```

- **Run with Docker Compose:**
  ```sh
  docker-compose up
  ``` 