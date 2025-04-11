"""This module defines the State class and its associated functionality.

The State class is a TypedDict that represents a state with a list of messages.
The `add_messages` function is used to define how the messages key should be updated.
"""

from typing import Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    """Represents a state with a list of messages.

    Attributes:
    ----------
    messages : Annotated[list, add_messages]
        A list of messages where the `add_messages` function defines how
        this key should be updated (appends messages to the list).
    """
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[Sequence[BaseMessage], add_messages]