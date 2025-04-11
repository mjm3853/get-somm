"""This module provides functionality to interact with a language model.

It includes:
- Initialization of the language model using `init_chat_model`.
- A `call_model` function to process messages using the language model.
"""

from typing import Any, Dict  # Add necessary imports for type hints

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.schema import SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

from agent.configuration import Configuration
from agent.logger import logger
from agent.state import State

load_dotenv()


# Define a Pydantic model for the cache
class LLMCache(BaseModel):
    """A cache for storing language model details.

    Attributes:
    ----------
    model : BaseChatModel | None
        The initialized language model instance.
    model_name : str | None
        The name of the language model.
    model_provider : str | None
        The provider of the language model.
    """
    model: BaseChatModel | None
    model_name: str | None
    model_provider: str | None

# Initialize the cache with the Pydantic model
_llm_cache = LLMCache(model=None, model_name=None, model_provider=None)

def call_model(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Call the language model with the given state.

    Parameters
    ----------
    state : State
        The state containing the messages to be processed by the language model.
    config : RunnableConfig
        The configuration for initializing the language model.

    Returns:
    -------
    Dict[str, Any]
        A dictionary containing the processed messages.
    """
    configuration = Configuration.from_runnable_config(config)
    system_prompt = configuration.system_prompt

    global _llm_cache

    # Check if the llm is already initialized and if the configuration has changed
    if (
        not _llm_cache.model
        or _llm_cache.model_name != configuration.model_name
        or _llm_cache.model_provider != configuration.model_provider
    ):
        # Initialize the chat model
        logger.info(f"Initializing language model: {configuration.model_name} from {configuration.model_provider}")
        llm = init_chat_model(configuration.model_name, model_provider=configuration.model_provider)

        # Update the cache using the Pydantic model
        _llm_cache = LLMCache(
            model=llm,
            model_name=configuration.model_name,
            model_provider=configuration.model_provider,
        )
    else:
        # Retrieve the llm from the cache
        logger.info(f"Retrieving language model from cache: {_llm_cache.model_name} from {_llm_cache.model_provider}")
        llm = _llm_cache.model

    # Create a SystemMessage from the system_prompt
    system_message = SystemMessage(content=system_prompt)

    return {"messages": [llm.invoke([system_message] + list(state["messages"]))]}
