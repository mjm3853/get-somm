# Beads UI - Issue Tracker Web Interface

A simple web interface for viewing and managing Beads issues and their relationships.

## Features

- **📋 Issue Management**: View all issues with filtering by status, priority, and readiness
- **📊 Statistics Dashboard**: Real-time stats showing total, ready, in-progress, and blocked issues
- **🔗 Dependency Visualization**: See blocking relationships between issues
- **🔍 Smart Filtering**: Filter by status, priority, or view ready/blocked issues
- **📱 Responsive Design**: Works on desktop and mobile devices

## Quick Start

1. **Ensure Beads is initialized** in your project:
   ```bash
   bd init  # If not already done
   ```

2. **Start the backend server**:
   ```bash
   python beads-ui/server.py
   ```

3. **Open the web interface**:
   ```
   http://localhost:8080
   ```

## API Endpoints

The backend provides these REST API endpoints:

- `GET /api/issues` - Fetch all issues (supports filtering)
- `GET /api/dependencies` - Fetch all dependencies
- `GET /api/stats` - Get issue statistics

### Query Parameters for `/api/issues`:

- `status` - Filter by status (open, in_progress, blocked, closed)
- `priority` - Filter by priority (0-4)
- `view` - Special views (ready, blocked)

Example: `/api/issues?status=open&priority=0&view=ready`

## Database Schema

The UI reads directly from the Beads SQLite database:

- **issues table** - Core issue data
- **dependencies table** - Blocking/related relationships
- **ready_issues view** - Issues with no blocking dependencies
- **blocked_issues view** - Issues blocked by unresolved dependencies

## Architecture

```
┌─────────────────┐    HTTP     ┌─────────────────┐    SQLite    ┌──────────────┐
│                 │ ◄────────► │                 │ ◄─────────► │              │
│   Frontend      │             │   Python        │             │   Beads      │
│   (HTML/JS)     │             │   HTTP Server   │             │   Database   │
│                 │             │                 │             │              │
└─────────────────┘             └─────────────────┘             └──────────────┘
```

- **Frontend**: Vanilla HTML/CSS/JavaScript - no external dependencies
- **Backend**: Python HTTP server using only standard library
- **Database**: SQLite database managed by Beads CLI

## Development

The server automatically discovers the Beads database by looking for:

1. `.beads/*.db` in current directory or parent directories
2. `~/.beads/default.db` as fallback

### Customization

- **Styling**: Modify CSS in `index.html`
- **API**: Extend endpoints in `server.py`
- **Features**: Add new functionality to the JavaScript classes

### Dependencies

- **Python 3.6+** (uses only standard library)
- **Beads CLI** must be installed and initialized in the project

## Issue Priority Colors

- **P0 (Critical)**: Red - Must be fixed immediately
- **P1 (High)**: Orange - Important, should be addressed soon
- **P2 (Medium)**: Yellow - Normal priority
- **P3 (Low)**: Gray - Nice to have

## Status Indicators

- **Open**: Green - Ready to be worked on
- **In Progress**: Blue - Currently being worked on
- **Blocked**: Red - Cannot proceed due to dependencies
- **Closed**: Gray - Completed

## Integration with Beads CLI

This UI is read-only and displays data from the Beads database. Use the Beads CLI for:

- Creating issues: `bd create "Issue title"`
- Updating status: `bd update issue-id --status in_progress`
- Managing dependencies: `bd dep add issue-1 issue-2`
- Closing issues: `bd close issue-id`

The web interface will reflect changes made via the CLI when refreshed.