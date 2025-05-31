import asyncio
from dotenv import load_dotenv
import os

from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel


load_dotenv()

API_KEY = os.getenv("API_KEY") or ""
MODEL_NAME = os.getenv("MODEL_NAME") or ""
# ...existing code...
if not API_KEY or not MODEL_NAME:
    raise ValueError("Please set API_KEY, MODEL_NAME via env or code.")
# ...existing code...

set_tracing_disabled(disabled=True)


@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main(model: str, api_key: str):
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=LitellmModel(model=model, api_key=api_key),
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main(MODEL_NAME, API_KEY))
