from langgraph.pregel.remote import RemoteGraph
import asyncio

url = "http://localhost:8123"
graph_name = "agent"
remote_graph = RemoteGraph(graph_name, url=url)

async def main():
    # stream outputs from the graph
    async for chunk in remote_graph.astream({
        "messages": [{"role": "user", "content": "what's better, beer or wine"}]
    }):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())