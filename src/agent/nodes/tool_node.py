"""This module defines the tool_node function for processing tool calls.

It includes:
- A mapping of tools by name.
- The tool_node function, which processes tool calls in the given state and returns the resulting messages.
"""

import json
from typing import Dict, List

from langchain_core.messages import AIMessage, ToolMessage

from agent.state import State
from agent.tools.wine_reader import wine_reader
from agent.tools.beer_reader import beer_reader

tools = [wine_reader, beer_reader]
tools_by_name = {tool.name: tool for tool in tools}


# Define our tool node
def tool_node(state: State) -> Dict[str, List[ToolMessage]]:
    """Process the tool calls in the given state and return the resulting messages.

    Parameters
    ----------
    state : State
        The current state containing tool calls to process.

    Returns:
    -------
    dict
        A dictionary containing the processed tool messages.
    """
    if not isinstance(state["messages"][-1], AIMessage):
        return {"messages": []}
        
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}