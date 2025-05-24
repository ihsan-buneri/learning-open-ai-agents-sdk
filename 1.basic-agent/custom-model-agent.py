import asyncio
from dotenv import load_dotenv
import os

from openai import AsyncOpenAI
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    set_tracing_disabled,
)

load_dotenv()
BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or ""
MODEL_NAME = os.getenv("MODEL_NAME") or ""

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("Please set BASE_URL, API_KEY, MODEL_NAME via env  or code.")


"""
This example uses a custom provider for a specific agent. Steps:
1. Create a custom OpenAI client.
2. Create a `Model` that uses the custom client.
3. Set the `model` on the Agent.

"""
client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)  # custom client
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME, openai_client=client
)  # custom model
set_tracing_disabled(disabled=True)


@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        tools=[get_weather],
        model=model,  # set custom model
    )

    result = await Runner.run(
        agent,
        "What's the weather in Tokyo?",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
