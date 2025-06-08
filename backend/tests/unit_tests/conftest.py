from typing import ClassVar, List, Optional

import pytest
from langchain.schema import AIMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool

from agent.state import State


@pytest.fixture
def basic_config():
    return RunnableConfig(configurable={
        "model_name": "test-model",
        "model_provider": "test-provider",
        "head_somm_prompt": "You are a test assistant"
    })

@pytest.fixture
def basic_state():
    return State(messages=[
        HumanMessage(content="Hello"),
        AIMessage(content="Hi there!")
    ])


class MockChatModel(BaseChatModel):
    invoke_count: ClassVar[int] = 0
    last_messages: ClassVar[Optional[List[BaseMessage]]] = None

    def invoke(self, messages: List[BaseMessage], **kwargs) -> AIMessage:
        MockChatModel.invoke_count += 1
        MockChatModel.last_messages = messages
        return AIMessage(content="Test response")

    def _generate(self, *args, **kwargs):
        return AIMessage(content="Test response")

    def _llm_type(self) -> str:
        return "mock"

class MockChatModelWithTools(MockChatModel):
    bound_tools: ClassVar[Optional[List[BaseTool]]] = None

    def bind_tools(self, tools, **kwargs):
        # Store the tools for inspection if needed
        MockChatModelWithTools.bound_tools = tools
        # Return self to allow method chaining
        return self

@pytest.fixture
def mock_chat_model():
    # Reset tracking before each test
    MockChatModel.invoke_count = 0
    MockChatModel.last_messages = None
    return MockChatModel()

@pytest.fixture
def mock_chat_model_with_tools():
    return MockChatModelWithTools()
