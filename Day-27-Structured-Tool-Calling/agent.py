import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from schemas import TOOLS
from tools import TOOL_REGISTRY
from validator import validate_arguments


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna"
)


SYSTEM_PROMPT = """
You are a helpful AI agent.

You have access to four tools:

1. search_documents
2. get_weather_stub
3. calculate
4. get_today

Use tools whenever they are necessary.

Do not invent tool results.

After receiving tool results, decide whether another tool is needed.

For multi-step questions, perform the required tools in sequence.

Give a concise final answer based on the actual tool results.
"""


def execute_tool(tool_name: str, arguments: dict):
    """
    Validate and execute a tool safely.
    """

    valid, message = validate_arguments(
        tool_name,
        arguments
    )

    if not valid:
        return {
            "error": message
        }

    try:
        function = TOOL_REGISTRY[tool_name]

        result = function(**arguments)

        return result

    except Exception as exc:
        return {
            "error": str(exc)
        }


def run_agent(question: str):

    conversation = [
        {
            "role": "user",
            "content": question,
        }
    ]

    tool_calls_log = []

    for _ in range(10):

        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=conversation,
            tools=TOOLS,
            parallel_tool_calls=False,
        )

        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # No tool call means the model has produced
        # the final answer.
        if not function_calls:

            return {
                "answer": response.output_text,
                "tool_calls": tool_calls_log,
            }

        # Add model output to conversation.
        conversation.extend(response.output)

        for call in function_calls:

            tool_name = call.name

            arguments = json.loads(
                call.arguments
            )

            print("\n[TOOL CALL]")
            print(f"Tool: {tool_name}")
            print(f"Arguments: {arguments}")

            result = execute_tool(
                tool_name,
                arguments
            )

            print(f"Result: {result}")

            tool_calls_log.append(
                {
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result,
                    "call_id": call.call_id,
                }
            )

            conversation.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(
                        result,
                        default=str
                    ),
                }
            )

    raise RuntimeError(
        "Maximum tool-call loop reached."
    )


if __name__ == "__main__":

    question = input(
        "Enter your question: "
    )

    result = run_agent(question)

    print("\n====================")
    print("FINAL ANSWER")
    print("====================")

    print(result["answer"])

    print("\n====================")
    print("TOOL CALLS")
    print("====================")

    for call in result["tool_calls"]:

        print(
            f"\nTool: {call['tool']}"
        )

        print(
            f"Arguments: {call['arguments']}"
        )

        print(
            f"Result: {call['result']}"
        )