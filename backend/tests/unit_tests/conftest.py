from typing import Any, Callable, ClassVar, Dict, List, Optional, Sequence, Union

import pytest
from langchain.schema import AIMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from typing_extensions import override

from agent.state import State


@pytest.fixture
def basic_config() -> RunnableConfig:
    return RunnableConfig(configurable={
        "model_name": "test-model",
        "model_provider": "test-provider",
        "beverage_director_prompt": "You are a test assistant"
    })

@pytest.fixture
def basic_state() -> State:
    return State(messages=[
        HumanMessage(content="Hello"),
        AIMessage(content="Hi there!")
    ])


class MockChatModel(BaseChatModel):
    invoke_count: ClassVar[int] = 0
    last_messages: ClassVar[Optional[List[BaseMessage]]] = None

    @override
    def invoke(self, input: Union[PromptValue, str, Sequence[Union[BaseMessage, List[str], tuple[str, str], str, Dict[str, Any]]]], config: Optional[RunnableConfig] = None, *, stop: Optional[List[str]] = None, **kwargs: Any) -> AIMessage:
        MockChatModel.invoke_count += 1
        if isinstance(input, list) and all(isinstance(item, BaseMessage) for item in input):
            MockChatModel.last_messages = input
        elif isinstance(input, BaseMessage):
            MockChatModel.last_messages = [input]
        elif isinstance(input, str):
            MockChatModel.last_messages = [HumanMessage(content=input)]
        else:
            # Handle other types like PromptValue
            MockChatModel.last_messages = [HumanMessage(content=str(input))]
        return AIMessage(content="Test response")

    def _generate(self, *args: Any, **kwargs: Any) -> Any:
        return AIMessage(content="Test response")

    @property
    def _llm_type(self) -> str:
        return "mock"

class MockChatModelWithTools(MockChatModel):
    bound_tools: ClassVar[Optional[Sequence[Union[Dict[str, Any], type, Callable[..., Any], BaseTool]]]] = None

    @override
    def bind_tools(self, tools: Sequence[Union[Dict[str, Any], type, Callable[..., Any], BaseTool]], *, tool_choice: Optional[str] = None, **kwargs: Any) -> 'MockChatModelWithTools':
        # Store the tools for inspection if needed
        MockChatModelWithTools.bound_tools = tools
        # Return self to allow method chaining
        return self

@pytest.fixture
def mock_chat_model() -> MockChatModel:
    # Reset tracking before each test
    MockChatModel.invoke_count = 0
    MockChatModel.last_messages = None
    return MockChatModel()

@pytest.fixture
def mock_chat_model_with_tools() -> MockChatModelWithTools:
    return MockChatModelWithTools()
