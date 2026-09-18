import json
import ast
import operator
from datetime import datetime


# ============================================================
# 1. CALCULATOR TOOL
# ============================================================

def calculator(expression: str) -> str:
    """
    Safely evaluate basic arithmetic expressions.
    """

    try:
        tree = ast.parse(expression, mode="eval")

        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }

        def evaluate(node):

            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value

                raise ValueError("Only numbers are allowed.")

            if isinstance(node, ast.BinOp):

                left = evaluate(node.left)
                right = evaluate(node.right)

                operation = allowed_operators.get(type(node.op))

                if operation is None:
                    raise ValueError("Operator not allowed.")

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):

                operand = evaluate(node.operand)

                if isinstance(node.op, ast.USub):
                    return -operand

                if isinstance(node.op, ast.UAdd):
                    return operand

                raise ValueError("Unary operator not allowed.")

            raise ValueError("Invalid expression.")

        result = evaluate(tree)

        return str(result)

    except Exception as e:
        return f"Calculator error: {e}"


# ============================================================
# 2. SEARCH DOCUMENTS TOOL
# ============================================================

def search_docs(query: str) -> str:
    """
    Search the local knowledge base.
    """

    try:

        with open(
            "knowledge_base.json",
            "r",
            encoding="utf-8"
        ) as file:

            documents = json.load(file)

        query_words = set(query.lower().split())

        results = []

        for document in documents:

            text = (
                document["title"]
                + " "
                + document["content"]
            ).lower()

            score = sum(
                1
                for word in query_words
                if word in text
            )

            if score > 0:
                results.append(
                    (score, document)
                )

        results.sort(
            key=lambda x: x[0],
            reverse=True
        )

        if not results:
            return "No relevant documents found."

        output = []

        for score, document in results[:3]:

            output.append(
                f"Title: {document['title']}\n"
                f"Content: {document['content']}"
            )

        return "\n\n".join(output)

    except FileNotFoundError:

        return "Search error: knowledge_base.json not found."

    except Exception as e:

        return f"Search error: {e}"


# ============================================================
# 3. TODAY'S DATE TOOL
# ============================================================

def get_today(_: str = "") -> str:
    """
    Return today's date.
    """

    return datetime.now().strftime("%Y-%m-%d")


# ============================================================
# TOOL REGISTRY
# ============================================================

tool_registry = {
    "calculator": calculator,
    "search_docs": search_docs,
    "get_today": get_today
}


# ============================================================
# TOOL DISPATCHER
# ============================================================

def dispatch_tool(tool_name: str, argument: str) -> str:
    """
    Find and execute the requested tool.
    """

    if tool_name not in tool_registry:

        return f"Tool error: Unknown tool '{tool_name}'"

    tool = tool_registry[tool_name]

    return tool(argument)