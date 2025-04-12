"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph

from agent.configuration import Configuration
from agent.nodes.head_somm import head_somm
from agent.nodes.tool_node import tool_node
from agent.state import State


# Define the conditional edge that determines whether to continue or not
def should_continue(state: State) -> str:
    """Determine the next step in the workflow based on the state.

    Parameters
    ----------
    state : State
        The current state of the workflow, containing messages and tool calls.

    Returns:
    -------
    str
        "end" if there are no tool calls in the last message, otherwise "continue".
    """
    messages = state["messages"]
    last_message = messages[-1]
    # Only check for tool calls if the message is from the AI
    if not isinstance(last_message, AIMessage):
        return "end"
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    return "continue"

# Define a new graph
workflow = StateGraph(State, config_schema=Configuration)

# Add the node to the graph
workflow.add_node("head_somm", head_somm)
workflow.add_node("tools", tool_node)

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "head_somm",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    {
        # If `tools`, then we call the tool node.
        "continue": "tools",
        # Otherwise we finish.
        "end": "__end__",
    },
)


# Set the entrypoint as `call_model`
workflow.add_edge("__start__", "head_somm")
workflow.add_edge("tools", "head_somm") 

# Compile the workflow into an executable graph
graph = workflow.compile()
graph.name = "BirdSomm"  # This defines the custom name in LangSmith
