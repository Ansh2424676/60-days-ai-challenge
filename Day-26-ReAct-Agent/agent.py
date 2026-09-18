import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from tools import dispatch_tool


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found in .env file."
    )

client = OpenAI(api_key=api_key)


# ============================================================
# MODEL
# ============================================================

MODEL = "gpt-5.6-luna"


# ============================================================
# REACT SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a manual ReAct-style AI agent.

Your job is to solve the user's problem by reasoning,
selecting tools, executing actions, observing results,
and continuing until you can provide a final answer.

Available tools:

1. calculator
   - Performs arithmetic calculations.
   - Input: arithmetic expression.

2. search_docs
   - Searches the local knowledge base.
   - Input: search query.

3. get_today
   - Returns today's date.
   - Input: empty string.

You MUST follow this format:

Thought: <brief reason for the next step>
Action: <tool name>
Action Input: <tool argument>

After the tool executes, you will receive:

Observation: <actual tool result>

Then continue with another Thought and Action if needed.

When the task is complete, output:

Final Answer: <answer>

Rules:

- Use the appropriate tool for the task.
- Never invent a tool result.
- Only use information contained in actual observations.
- Do not call tools unnecessarily.
- Stop when the task is complete.
"""


# ============================================================
# ACTION PARSER
# ============================================================

def parse_action(response: str):
    """
    Extract the tool name and tool input
    from the LLM response.
    """

    action_match = re.search(
        r"Action:\s*(.+)",
        response
    )

    input_match = re.search(
        r"Action Input:\s*(.+)",
        response
    )

    if not action_match:
        return None, None

    action = action_match.group(1).strip()

    argument = ""

    if input_match:
        argument = input_match.group(1).strip()

    return action, argument


# ============================================================
# REACT AGENT
# ============================================================

def run_agent(question: str, max_steps: int = 8):

    print("\n" + "=" * 80)
    print("USER QUESTION")
    print("=" * 80)
    print(question)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    trace = []

    for step in range(1, max_steps + 1):

        print("\n" + "-" * 80)
        print(f"STEP {step}")
        print("-" * 80)

        response = client.responses.create(
            model=MODEL,
            input=messages
        )

        output = response.output_text.strip()

        print(output)

        trace.append(output)

        # ----------------------------------------------------
        # Check Final Answer
        # ----------------------------------------------------

        if "Final Answer:" in output:

            print("\n" + "=" * 80)
            print("AGENT COMPLETED")
            print("=" * 80)

            return trace

        # ----------------------------------------------------
        # Parse Action
        # ----------------------------------------------------

        action, argument = parse_action(output)

        if not action:

            error = (
                "ERROR: No valid Action was found "
                "in the model response."
            )

            print(error)
            trace.append(error)

            break

        # ----------------------------------------------------
        # Execute Tool
        # ----------------------------------------------------

        print("\nTOOL EXECUTION")
        print(f"Tool: {action}")
        print(f"Input: {argument}")

        observation = dispatch_tool(
            action,
            argument
        )

        print(f"Observation: {observation}")

        trace.append(
            f"Observation: {observation}"
        )

        # ----------------------------------------------------
        # Send observation back to LLM
        # ----------------------------------------------------

        messages.append(
            {
                "role": "assistant",
                "content": output
            }
        )

        messages.append(
            {
                "role": "user",
                "content": (
                    f"Observation: {observation}\n\n"
                    "Continue the ReAct process."
                )
            }
        )

    # --------------------------------------------------------
    # Maximum steps reached
    # --------------------------------------------------------

    error = (
        f"Agent stopped after reaching the "
        f"maximum of {max_steps} steps."
    )

    print("\n" + "=" * 80)
    print(error)
    print("=" * 80)

    trace.append(error)

    return trace


# ============================================================
# FIVE MULTI-STEP TEST PROBLEMS
# ============================================================

problems = [

    """
    First retrieve the definition of RAG from the
    knowledge base. Then calculate 25% of 800.
    Use both tools before answering.
    """,

    """
    First retrieve the definition of FAISS from the
    knowledge base. Then calculate 15 * 40.
    Use both tools before answering.
    """,

    """
    First retrieve information about AI agents.
    Then calculate 1200 / 8.
    Use both tools before answering.
    """,

    """
    First retrieve information about FastAPI.
    Then use the date tool to find today's date.
    Use both tools before answering.
    """,

    """
    First retrieve information about machine learning.
    Then calculate 30% of 1500.
    Use both tools before answering.
    """
]


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    all_traces = []

    for index, problem in enumerate(
        problems,
        start=1
    ):

        print("\n\n")
        print("#" * 80)
        print(f"PROBLEM {index}")
        print("#" * 80)

        trace = run_agent(problem)

        all_traces.append(
            {
                "problem_number": index,
                "question": problem.strip(),
                "trace": trace
            }
        )

    # --------------------------------------------------------
    # Save traces
    # --------------------------------------------------------

    os.makedirs(
        "results",
        exist_ok=True
    )

    with open(
        "results/traces.txt",
        "w",
        encoding="utf-8"
    ) as file:

        for item in all_traces:

            file.write(
                "\n" + "=" * 80 + "\n"
            )

            file.write(
                f"PROBLEM {item['problem_number']}\n"
            )

            file.write(
                "=" * 80 + "\n\n"
            )

            file.write(
                item["question"] + "\n\n"
            )

            for trace_item in item["trace"]:

                file.write(
                    trace_item + "\n\n"
                )

    print("\n")
    print("=" * 80)
    print("ALL TRACES SAVED")
    print("results/traces.txt")