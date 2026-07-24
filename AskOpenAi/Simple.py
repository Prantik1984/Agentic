import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner,trace


async def main():
    with trace("Simple Nutrition Agent"):
        nutrition_agent = Agent(
            name="Assistant",
            instructions="You are a helpful assistant.",
        )

        query = "How healthy are bananas?"

        result = await Runner.run(nutrition_agent, query)
        print(result.final_output)

if __name__=='__main__':
    load_dotenv()
    asyncio.run(main())