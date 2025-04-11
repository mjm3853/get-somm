import pytest
from langchain.schema import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from agent.state import State


@pytest.fixture
def basic_config():
    return RunnableConfig(configurable={
        "model_name": "test-model",
        "model_provider": "test-provider",
        "system_prompt": "You are a test assistant"
    })

@pytest.fixture
def basic_state():
    return State(messages=[
        HumanMessage(content="Hello"),
        AIMessage(content="Hi there!")
    ])
