"""Define the configurable parameters for the agent."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, fields
from typing import Optional

from langchain_core.runnables import RunnableConfig

from agent.prompts.beverage_director import BEVERAGE_DIRECTOR_PROMPT
from agent.prompts.head_somm import HEAD_SOMM_PROMPT


@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    # Add configurable values here!
    # these values can be pre-set when you
    # create assistants (https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/)
    # and when you invoke the graph
    model_name: str = "claude-3-5-sonnet-latest"
    model_provider: str = "anthropic"
    head_somm_prompt: str = field(
        default=HEAD_SOMM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )
    beverage_director_prompt: str = field(
        default=BEVERAGE_DIRECTOR_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )
    session_id: str = field(
        default=str(uuid.uuid4()),
        metadata={
            "description": "The session ID for the agent's interactions. "
            "This ID is used to track the agent's interactions across sessions."
        },
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        configurable = (config.get("configurable") or {}) if config else {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})
