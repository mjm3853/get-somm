"""This module provides functionality to interact with a language model.

It includes:
- Initialization of the language model using `init_chat_model`.
- A `call_model` function to process messages using the language model.
"""

import logging

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig

from agent.configuration import Configuration
from agent.logger import setup_logging
from agent.state import State

load_dotenv()

# Configure logging
setup_logging()

# Module-level cache for the language model
_llm_cache = {"model": None, "model_name": None, "model_provider": None}


def call_model(state: State, config: RunnableConfig):
    """Call the language model with the given state.

    Parameters
    ----------
    state : State
        The state containing the messages to be processed by the language model.
    """
    configuration = Configuration.from_runnable_config(config)

    global _llm_cache

    # Check if the llm is already initialized and if the configuration has changed
    if (
        _llm_cache["model"] is None
        or _llm_cache["model_name"] != configuration.model_name
        or _llm_cache["model_provider"] != configuration.model_provider
    ):
        # Initialize the chat model
        logging.info(f"Initializing language model: {configuration.model_name} from {configuration.model_provider}")
        llm = init_chat_model(configuration.model_name, model_provider=configuration.model_provider)

        # Store the llm and configuration in the cache
        _llm_cache["model"] = llm
        _llm_cache["model_name"] = configuration.model_name
        _llm_cache["model_provider"] = configuration.model_provider
    else:
        # Retrieve the llm from the cache
        logging.info(f"Retrieving language model from cache: {_llm_cache['model_name']} from {_llm_cache['model_provider']}")
        llm = _llm_cache["model"]

    return {"messages": [llm.invoke(state["messages"])]}
