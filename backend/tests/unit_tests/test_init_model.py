from typing import ClassVar, List, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage

from agent.utils.init_model import LLMCache, init_model


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


def test_init_model_basic(mocker, basic_config, mock_chat_model):
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
