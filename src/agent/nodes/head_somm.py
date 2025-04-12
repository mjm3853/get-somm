"""This module defines the `head_somm` function, which initializes a model."""

from typing import Any, Dict  # Add necessary imports for type hints

from langchain.schema import SystemMessage
from langchain_core.runnables import RunnableConfig

from agent.configuration import Configuration
from agent.state import State
from agent.tools.wine_reader import wine_reader
from agent.utils.init_model import init_model


def head_somm(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Initialize and invoke a model with the given state and configuration.

    Parameters
    ----------
    state : State
        The current state containing messages and other context.
    config : RunnableConfig
        The configuration for initializing the model.

    Returns:
    -------
    Dict[str, Any]
        A dictionary containing the model's response messages.
    """
    configuration = Configuration.from_runnable_config(config)
    system_prompt = configuration.head_somm_prompt
    # Create a SystemMessage from the system_prompt
    system_message = SystemMessage(content=system_prompt)
    model = init_model(config)
    model_with_tools = model.bind_tools(
        tools=[wine_reader]
    )

    return {"messages": [model_with_tools.invoke([system_message] + list(state["messages"]))]}
