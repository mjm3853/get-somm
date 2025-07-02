import json
from typing import Any, List, Optional

from deepeval import evaluate
from deepeval.metrics import (  # type: ignore[attr-defined]
    TaskCompletionMetric,
    ToolCorrectnessMetric,
)
from deepeval.test_case import LLMTestCase, ToolCall
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, ToolMessage

from agent.graph import graph

load_dotenv()

# Set this to True to enable debug prints
DEBUG = False


def extract_tool_calls(messages: List[Any]) -> List[ToolCall]:
    """
    Extracts DeepEval ToolCall objects from a list of messages (AIMessage and ToolMessage).
    Matches tool_calls in AIMessage(s) to their corresponding ToolMessage outputs.
    """
    tool_msgs = [m for m in messages if isinstance(m, ToolMessage)]
    ai_msgs = [m for m in messages if isinstance(m, AIMessage)]
    tool_calls: List[ToolCall] = []
    for ai_msg in ai_msgs:
        for tool_call in getattr(ai_msg, "tool_calls", []):
            # Find the matching ToolMessage by tool_call_id
            tool_msg = next(
                (
                    tm
                    for tm in tool_msgs
                    if getattr(tm, "tool_call_id", None) == tool_call["id"]
                ),
                None,
            )
            if tool_msg and isinstance(tool_msg.content, str):
                try:
                    output_content = json.loads(tool_msg.content)
                except json.JSONDecodeError:
                    output_content = tool_msg.content
            else:
                output_content = tool_msg.content if tool_msg else None
            import logging
            logging.debug(
                "Tool output: %s",
                json.dumps(output_content, indent=2) if output_content else None,
            )
            tool_calls.append(
                ToolCall(
                    name=tool_call["name"],
                    description="(fill in from your tool registry or hardcode)",
                    input_parameters=tool_call.get("args", {}),
                    output=output_content,
                )
            )
    return tool_calls


def extract_ai_message_content(messages: List[Any]) -> str:
    """
    Extracts the user-facing content from the last AIMessage in the messages list.
    Handles both string and list-of-dict content formats.
    """
    ai_msgs = [m for m in messages if isinstance(m, AIMessage)]
    if not ai_msgs:
        return ""
    content = ai_msgs[-1].content
    if isinstance(content, list):
        # Join all 'text' fields from dicts in the list
        return " ".join(
            [c["text"] for c in content if isinstance(c, dict) and "text" in c]
        )
    return content


def create_test_case(
    user_input: str,
    expected_output: str,
    expected_tools: Optional[List[str]] = None,
    debug: bool = False,
) -> LLMTestCase:
    """
    Runs the agent graph with a user message and constructs a DeepEval LLMTestCase.
    Optionally checks for expected tool calls.
    """
    output = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
    messages = output["messages"]
    import logging
    logging.debug("All messages: %s", messages)
    tools_called = extract_tool_calls(messages)
    logging.debug("Extracted tools_called: %s", tools_called)
    ai_message_content = extract_ai_message_content(messages)
    # If expected_tools is provided, you could add assertions or checks here if desired
    return LLMTestCase(
        input=user_input,
        actual_output=ai_message_content,
        expected_output=expected_output,
        expected_tools=expected_tools,
        tools_called=tools_called,
    )


# Define the evaluation metric for task completion
metric = TaskCompletionMetric(threshold=0.7, model="gpt-4o", include_reason=True)
tool_metric = ToolCorrectnessMetric()

# Create the first test case using the new signature
test_case_1 = create_test_case(
    user_input="What's a good wine to start with?",
    expected_output="To help you get started with wine, I'd like to recommend a few approachable options. Before I make specific suggestions, it would help me to know...",
    expected_tools=[ToolCall(name="wine_reader", input_parameters={})],
    debug=True,
)

# Example of a manually constructed test case with multiple tools

# To run metric as a standalone
# metric.measure(test_case)
# print(metric.score, metric.reason)

# Evaluate the test cases using the defined metric
evaluate(test_cases=[test_case_1], metrics=[metric, tool_metric])
