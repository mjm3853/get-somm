from typing import Any, ClassVar, Dict, List, Optional, Sequence, Union

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnableConfig
from typing_extensions import override

from agent.utils.init_model import LLMCache, init_model


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


def test_init_model_basic(mocker: Any, basic_config: RunnableConfig, mock_chat_model: MockChatModel) -> None:
    """Test basic model initialization and caching."""
    # Reset cache with anthropic provider
    mocker.patch(
        "agent.utils.init_model._llm_cache",
        LLMCache(model=None, model_name=None, model_provider=None),
    )

    # Setup mocks
    mock_init_chat = mocker.patch(
        "agent.utils.init_model.init_chat_model", return_value=mock_chat_model
    )

    # First call - should initialize model
    model1 = init_model(basic_config)

    # Verify model initialization with correct provider
    mock_init_chat.assert_called_once_with("test-model", model_provider="test-provider")
    assert model1 == mock_chat_model

    # Second call - should use cached model
    model2 = init_model(basic_config)

    # Verify no new initialization
    mock_init_chat.assert_called_once()
    assert model1 == model2
