"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from langgraph.graph import StateGraph

from agent.configuration import Configuration
from agent.nodes.head_somm import head_somm
from agent.state import State

# Define a new graph
workflow = StateGraph(State, config_schema=Configuration)

# Add the node to the graph
workflow.add_node("head_somm", head_somm)

# Set the entrypoint as `call_model`
workflow.add_edge("__start__", "head_somm")

# Compile the workflow into an executable graph
graph = workflow.compile()
graph.name = "BirdSomm"  # This defines the custom name in LangSmith
