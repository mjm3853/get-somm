# get-somm

AI Somm — Monorepo for an AI-powered sommelier assistant.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- Node.js (for UI)
- **Moonrepo** (monorepo task/dependency manager)
  - Install globally: `npm install -g @moonrepo/cli`
  - Or use npx: `npx moon --version` (downloads and runs Moonrepo as needed)
  - See: https://moonrepo.dev/docs/install

## Project Structure

- `backend/` — LangGraph agent (backend). See [`backend/README.md`](backend/README.md) for backend setup, configuration, and commands.
- `frontend/` — Next.js UI frontend. See [`frontend/README.md`](frontend/README.md) for frontend setup and commands.
- **All monorepo tasks and scripts are managed with Moonrepo.**

## Monorepo Tasks

## Setup Backend and Frontend

`moon run :install`

### Run Backend and Frontend

`moon run :dev`

### More info

- Use [Moonrepo](https://moonrepo.dev/docs) to manage tasks across projects:
  - Run a task in a specific project: `moon run <project>:<task>`
  - Run a task across all projects: `moon run :<task>`
