import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner,trace,function_tool

@function_tool
def get_food_calories(food_item: str) -> int:
    """
    Get calorie data about food item

    Args:
        food_item:Nae of the fool (example:-apple,banana)

    Returns:
        Calorie information per serving
    """
    calorie_data={
        "apple":10,
        "banana":20,
        "orange":30,

    }
    food_key=food_item.lower()
    if food_key in calorie_data.keys():
        return f"{food_key} has {calorie_data[food_key]} calories"
    else:
        return f"Can't find calories for {food_key}"

calorie_agent=Agent(
    name="Nutritional Agent",
    instructions=""""
    You are a helpful nutrition assistant giving out calorie information.
    You give helpful and  concise answers
    """,
    tools=[get_food_calories],
)

async def main():
    question="I have eaten 10 bananas. How many calories have I consumed"
    with trace("Nutrition agent with tools"):
        result = await Runner.run(calorie_agent,question)
        print(result.final_output)


if __name__=='__main__':
    load_dotenv()
    asyncio.run(main())