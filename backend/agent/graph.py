"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langgraph.graph import StateGraph

from agent.configuration import Configuration
from agent.nodes.head_somm import head_somm
from agent.nodes.tool_node import tool_node
from agent.state import State

load_dotenv()

langfuse = get_client()

langfuse_handler = CallbackHandler()


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

# Add nodes for the sommelier agent and tool executor
workflow.add_node("head_somm", head_somm)
workflow.add_node("tools", tool_node)

# Add conditional edges to control the flow between nodes
workflow.add_conditional_edges(
    # The source node is head_somm (the sommelier agent)
    "head_somm",
    # Function that checks if we need to execute tools
    should_continue,
    {
        # If tools are requested, route to the tool executor
        "continue": "tools",
        # If no tools needed, end the conversation
        "end": "__end__",
    },
)

# Configure the workflow edges
workflow.add_edge("__start__", "head_somm")  # Start with the sommelier agent
workflow.add_edge("tools", "head_somm")  # Return to agent after tool execution

# Create the executable graph
graph = workflow.compile().with_config({"callbacks": [langfuse_handler]})
graph.name = "GetSomm"  # Name for tracking in LangSmith
