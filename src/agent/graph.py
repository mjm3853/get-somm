"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from langgraph.graph import StateGraph

from agent.configuration import Configuration
from agent.nodes.call_model import call_model
from agent.state import State

# Define a new graph
workflow = StateGraph(State, config_schema=Configuration)

# Add the node to the graph
workflow.add_node("call_model", call_model)

# Set the entrypoint as `call_model`
workflow.add_edge("__start__", "call_model")

# Compile the workflow into an executable graph
graph = workflow.compile()
graph.name = "Somm"  # This defines the custom name in LangSmith
