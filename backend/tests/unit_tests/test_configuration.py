from langchain_core.runnables import RunnableConfig

from agent.configuration import Configuration


def test_configuration_defaults() -> None:
    config = Configuration()
    assert config.model_name == "claude-3-5-sonnet-latest"
    assert config.model_provider == "anthropic"
    assert config.head_somm_prompt is not None


def test_configuration_from_runnable_config(basic_config: RunnableConfig) -> None:
    config = Configuration.from_runnable_config(basic_config)
    assert config.model_name == "test-model"
    assert config.model_provider == "test-provider"
    assert config.beverage_director_prompt == "You are a test assistant"


def test_configuration_empty() -> None:
    config = Configuration.from_runnable_config(None)
    assert isinstance(config, Configuration)
