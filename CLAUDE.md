# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Get-somm is a full-stack AI sommelier application using a monorepo structure. It combines a Python LangGraph backend with a Next.js frontend to provide intelligent wine and beverage recommendations.

### Architecture

- **Backend**: Python 3.11+ with LangGraph agent framework, using uv for dependency management
- **Frontend**: Next.js 15 with TypeScript, assistant-ui for chat interface, Tailwind CSS
- **Monorepo**: Managed with Moonrepo for cross-project task coordination
- **AI Framework**: LangGraph for agent workflows, with Anthropic Claude as the LLM
- **Data**: CSV files for wine/beer lists, synthetic datasets for evaluation

## Development Commands

### Monorepo Tasks (Moonrepo)
```bash
# Install all dependencies across projects
moon run :install

# Run both backend and frontend in development
moon run :dev

# Run specific project task
moon run <project>:<task>
```

### Backend (Python/LangGraph)
```bash
# Navigate to backend directory first
cd backend

# Install dependencies
uv sync

# Start LangGraph development server
uv run langgraph dev

# Run tests with coverage
uv run pytest

# Run linting
uv run ruff check
uv run ruff format

# Build Docker image
uv run langgraph build

# Run with Docker Compose (Redis + Postgres + API)
docker-compose up
```

### Frontend (Next.js)
```bash
# Navigate to frontend directory first
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint

# Check for dependency updates
npx npm-check-updates
npx npm-check-updates -u
```

## Code Architecture

### Backend Structure (`backend/`)
- **`agent/`**: Core LangGraph agent implementation
  - `graph.py`: Main workflow definition with sommelier agent and tool nodes
  - `state.py`: Agent state schema
  - `configuration.py`: Configuration management
  - `nodes/`: Individual workflow nodes (head_somm, tool_node)
  - `prompts/`: LLM prompts for different agent roles
  - `tools/`: Custom tools for wine/beer data access
  - `utils/`: Utility functions and model initialization
- **`tests/`**: Comprehensive test suite
  - `unit_tests/`: pytest-based unit tests
  - `deep_eval/`: DeepEval framework for LLM evaluation
  - `reports/`: Coverage and test reports (HTML output)
- **`synthetic_data/`**: Generated datasets for testing and evaluation
- **`langgraph.json`**: LangGraph configuration for graphs and environment

### Frontend Structure (`frontend/`)
- **`app/`**: Next.js app directory structure
  - `api/[...path]/route.ts`: Proxy API routes to backend
  - `page.tsx`: Main chat interface
  - `layout.tsx`: App layout and global styles
- **`components/`**: React components
  - `MyAssistant.tsx`: Main assistant chat component
  - `assistant-ui/`: Custom assistant-ui components
  - `ui/`: Reusable UI components (shadcn/ui style)
- **`lib/`**: Utilities and API clients
  - `chatApi.ts`: Backend communication layer
  - `utils.ts`: General utility functions

### Agent Workflow
The LangGraph agent follows this pattern:
1. **head_somm**: Main sommelier agent that processes user requests
2. **should_continue**: Conditional logic to determine if tools are needed
3. **tools**: Tool execution node for data retrieval
4. **Cycle**: Returns to head_somm until no more tools needed

## Environment Variables

### Backend (`.env`)
```bash
ANTHROPIC_API_KEY=your_anthropic_key
LANGFUSE_SECRET_KEY=your_langfuse_key  # For LLM observability
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
```

### Frontend (`.env.local`)
```bash
LANGCHAIN_API_KEY=your_langchain_api_key
LANGGRAPH_API_URL=your_langgraph_api_url
NEXT_PUBLIC_LANGGRAPH_ASSISTANT_ID=your_assistant_id
```

## Testing Strategy

### Backend Testing
- **pytest** with async support for LangGraph workflows
- **pytest-cov** for coverage reporting (HTML reports in `tests/reports/`)
- **pytest-mock** for mocking external dependencies
- **DeepEval** framework for LLM response evaluation
- Coverage targets: agent logic, tool functionality, configuration

### Frontend Testing
- Standard Next.js testing patterns with Jest/React Testing Library
- Focus on component behavior and API integration

## Code Quality Tools

### Backend (Python)
- **ruff**: Linting and formatting (PEP8, pyflakes, isort, pydocstyle)
- **mypy**: Type checking
- Configuration in `pyproject.toml`

### Frontend (TypeScript)
- **ESLint**: Code linting with Next.js config
- **TypeScript**: Strict type checking
- Configuration in `eslint.config.mjs` and `tsconfig.json`

## Development Workflow

1. **Setup**: Run `moon run :install` from project root
2. **Development**: Use `moon run :dev` to start both services
3. **Testing**: Run backend tests with `uv run pytest` from backend/
4. **Linting**: Use project-specific linters before committing
5. **Docker**: Use `docker-compose up` for full environment with databases

## Key Dependencies

### Backend
- **LangGraph**: Agent framework and workflow orchestration
- **LangChain**: LLM integrations and tooling
- **Anthropic**: Claude LLM provider
- **Langfuse**: LLM observability and monitoring
- **pandas**: Data manipulation for wine/beer datasets
- **DeepEval**: LLM evaluation framework

### Frontend
- **Next.js 15**: React framework with app directory
- **assistant-ui**: Specialized chat interface components
- **Radix UI**: Accessible UI component primitives
- **Tailwind CSS**: Utility-first styling
- **Zustand**: State management

## Docker Services
- **API**: Main LangGraph application (port 8123)
- **Redis**: Caching and session storage
- **Postgres**: Persistent data storage (port 5433)

## Performance Considerations
- LangGraph development server supports hot reloading
- Frontend uses Next.js Turbopack for faster development builds
- Docker Compose provides full production-like environment
- Coverage reports and test results are generated as HTML for easy review