from typing import ClassVar, List, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage

from agent.nodes.call_model import call_model


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

def test_call_model_basic(mocker, basic_config, basic_state):
    # Reset tracking
    MockChatModel.invoke_count = 0
    MockChatModel.last_messages = None
    
    # Setup mocks
    mock_llm = MockChatModel()
    mock_init_chat = mocker.patch("agent.nodes.call_model.init_chat_model", return_value=mock_llm)
    
    # First call - should initialize model
    result = call_model(basic_state, basic_config)
    
    # Verify model initialization and invocation
    mock_init_chat.assert_called_once_with("test-model", model_provider="test-provider")
    assert mock_llm.invoke_count == 1
    assert isinstance(mock_llm.last_messages[0], SystemMessage)
    assert mock_llm.last_messages[1:] == basic_state["messages"]
    
    # Second call - should use cached model
    result2 = call_model(basic_state, basic_config)
    
    # Verify second invocation
    assert mock_llm.invoke_count == 2
    assert result == result2
