from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from agent.nodes.head_somm import head_somm
from agent.state import State


def test_head_somm(mocker, basic_config, mock_chat_model_with_tools):
    """Test head_somm function with basic configuration."""
    # Setup mock model
    mock_llm = mock_chat_model_with_tools
    mocker.patch("agent.nodes.head_somm.init_model", return_value=mock_llm)
    
    # Setup test state
    test_state: State = State(messages=[])
    test_config: RunnableConfig = basic_config
    
    # Call head_somm
    result = head_somm(test_state, test_config)
    
    # Verify result structure
    assert isinstance(result, dict)
    assert "messages" in result
    assert len(result["messages"]) == 1
    assert result["messages"][0].content == "Test response"
    
    # Verify model was called with correct system message
    assert mock_llm.last_messages is not None
    assert isinstance(mock_llm.last_messages[0], SystemMessage)
    assert mock_llm.last_messages[0].content == basic_config["configurable"]["head_somm_prompt"]
    
    # Verify tools were bound
    assert hasattr(mock_llm, 'bound_tools')
