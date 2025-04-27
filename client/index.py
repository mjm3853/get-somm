"""Client for interacting with the remote LangGraph agent."""

import asyncio

from langgraph.pregel.remote import RemoteGraph

from agent.logger import logger

url = "http://localhost:8123"
graph_name = "agent"
remote_graph = RemoteGraph(graph_name, url=url)

async def main():
    """Stream responses from the remote agent and log them."""
    # stream outputs from the graph
    async for chunk in remote_graph.astream({
        "messages": [{"role": "user", "content": "what's better, beer or wine"}]
    }):
        logger.info(chunk)

if __name__ == "__main__":
    asyncio.run(main())