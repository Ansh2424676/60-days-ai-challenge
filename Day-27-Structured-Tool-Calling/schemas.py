TOOLS = [
    {
        "type": "function",
        "name": "search_documents",
        "description": (
            "Search the local knowledge base for relevant documents. "
            "Use this when the user asks about stored technical information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The topic or question to search for.",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Maximum number of documents to return.",
                    "minimum": 1,
                    "maximum": 5,
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "get_weather_stub",
        "description": (
            "Get deterministic stub weather information for a city."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city.",
                }
            },
            "required": ["city"],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "calculate",
        "description": (
            "Calculate a basic mathematical expression."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "A mathematical expression such as "
                        "'25 / 100 * 800'."
                    ),
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "get_today",
        "description": "Get today's date and weekday.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
]