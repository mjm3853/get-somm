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
- **Beads** (dependency-aware issue tracker for task management)
  - See [installation guide](https://github.com/steveyegge/beads)
  - Initialize in project: `bd init` (creates `.beads/` directory)
  - Quick start: `bd quickstart` to learn the basics

## Project Structure

- `backend/` — LangGraph agent (backend). See [`backend/README.md`](backend/README.md) for backend setup, configuration, and commands.
- `frontend/` — Next.js UI frontend. See [`frontend/README.md`](frontend/README.md) for frontend setup and commands.
- `beads-ui/` — Web interface for viewing Beads issues and dependencies. See [`beads-ui/README.md`](beads-ui/README.md) for setup and usage.
- **All monorepo tasks and scripts are managed with Moonrepo.**

## Monorepo Tasks

## Setup Backend and Frontend

`moon run :install`

### Run Backend and Frontend

`moon run :dev`

### Run Beads Issue Tracker UI

View and manage project issues with a web interface:

```bash
# Start the Beads UI server
python beads-ui/server.py

# Open browser to http://localhost:8080
```

Features:
- 📊 Real-time issue statistics and filtering
- 🔗 Dependency relationship visualization
- 📱 Responsive design for desktop and mobile
- ⚡ Live data from Beads SQLite database

### More info

- Use [Moonrepo](https://moonrepo.dev/docs) to manage tasks across projects:
  - Run a task in a specific project: `moon run <project>:<task>`
  - Run a task across all projects: `moon run :<task>`
- Use [Beads CLI](https://github.com/steveyegge/beads) for issue tracking:
  - View ready work: `bd ready`
  - Create issues: `bd create "Issue title"`
  - Update status: `bd update issue-id --status in_progress`
