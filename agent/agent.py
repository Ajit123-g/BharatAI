import os
import json

from dotenv import load_dotenv
from mistralai.client import Mistral

from tools.weather import get_weather
from tools.news import search_news


load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

client = Mistral(
    api_key=MISTRAL_API_KEY
)


MODEL = "ministral-3b-2512"


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": (
                "Get the current weather of an Indian city. "
                "Use this whenever the user asks about weather, "
                "temperature, humidity, wind or weather conditions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Indian city name, for example Delhi, Lucknow or Mumbai."
                    }
                },
                "required": ["city"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_news",
            "description": (
                "Search the internet for current news and recent information. "
                "Use this whenever the user asks for news, latest events, "
                "recent developments or current information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "News search query."
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def run_agent(user_message):

    messages = [
        {
            "role": "system",
            "content": """
You are BharatAI, an AI assistant focused on India.

You have two tools:

1. get_weather(city)
   - Gets current weather for an Indian city.
   - Use this for weather-related questions.

2. search_news(query)
   - Searches the internet for current/recent news.
   - Use this for news-related questions.

IMPORTANT:

The user may request:

A. Weather only
Example:
"What's the weather in Delhi?"

→ Call get_weather only.

B. News only
Example:
"What are the latest AI news in India?"

→ Call search_news only.

C. Weather AND news
Example:
"What's the weather in Mumbai and what are today's news about Mumbai?"

→ Call BOTH get_weather and search_news.

You are allowed to call multiple tools for one user request.

Never invent current weather or current news.

After receiving tool results, combine them into one clear response.

For news, provide the article title and source URL when available.

For weather, clearly mention:
- City
- Temperature
- Feels like
- Weather condition
- Humidity
- Wind speed
"""
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    response = client.chat.complete(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    # No tool call
    if not assistant_message.tool_calls:
        return assistant_message.content

    # Add assistant's tool request
    messages.append(assistant_message)

    # Execute requested tools
    for tool_call in assistant_message.tool_calls:

        function_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        if function_name == "get_weather":

            result = get_weather(
                arguments["city"]
            )

        elif function_name == "search_news":

            result = search_news(
                arguments["query"]
            )

        else:
            result = {
                "error": f"Unknown tool: {function_name}"
            }

        messages.append({
            "role": "tool",
            "name": function_name,
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })

    # Ask Mistral to produce final answer
    final_response = client.chat.complete(
        model=MODEL,
        messages=messages
    )

    return final_response.choices[0].message.content