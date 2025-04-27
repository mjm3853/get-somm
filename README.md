# get-somm
AI Somm

## Prerequisites

- Python
- <https://docs.astral.sh/uv/>

## Setup

`uv sync`

Setup a `.env` with an Anthropic API Key

`uv run langgraph dev`

## Deploy with Docker Compose

`uv run langgraph build`

Get image name and add to .env

`docker-compose up`

Navigate to `http://localhost:8123/docs`

Or call via `uv run client/index.py`