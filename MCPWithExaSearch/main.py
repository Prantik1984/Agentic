
from agents import Agent,trace,Runner,function_tool
from Operators.db_operator import DBOperator
from agents.mcp import MCPServerStreamableHttp
import os
from dotenv import load_dotenv
db_operator = DBOperator()
import asyncio

@function_tool
def calorie_lookup_tool(query: str) -> str:
    """
    Look up calorie information for a single food item.

    Args:
        query: The food item to look up.

    Returns:
        Matching nutrition information per 100 grams.
    """
    return db_operator.query_db(query)


async def main():
    exa_api_key = os.getenv("EXA_API_KEY")

    if not exa_api_key:
        raise RuntimeError("EXA_API_KEY is missing from the environment.")

    async with MCPServerStreamableHttp(
            name="Exa Search",
            params={
                "url": f"https://mcp.exa.ai/mcp?exaApiKey={exa_api_key}",
                "timeout": 90,
            },
    ) as exa_server:
        agent = Agent(
            name="Nutrition Assistant",
            instructions="""
    * You are a helpful nutrition assistant giving out calorie information.
    * You give concise answers.
    * You follow this workflow:
        0) First, use the calorie_lookup_tool to get the calorie information of the ingredients. But only use the result if it's explicitly for the food requested in the query.
        1) If you couldn't find the exact match for the food or you need to look up the ingredients, search the EXA web to figure out the exact ingredients of the meal.
        Even if you have the calories in the web search response, you should still use the calorie_lookup_tool to get the calorie
        information of the ingredients to make sure the information you provide is consistent.
        2) Then, if necessary, use the calorie_lookup_tool to get the calorie information of the ingredients.
    * Even if you know the recipe of the meal, always use Exa Search to find the exact recipe and ingredients.
    * Once you know the ingredients, use the calorie_lookup_tool to get the calorie information of the individual ingredients.
    * If the query is about the meal, in your final output give a list of ingredients with their quantities and calories for a single serving. Also display the total calories.
    * Don't use the calorie_lookup_tool more than 10 times.
    """,
         mcp_servers=[exa_server],
         tools=[calorie_lookup_tool],
     )

     question = input("What do you want to know about nutrition? ")

     result = await Runner.run(
         agent,
         question,
     )

     print("\nAnswer:")
     print(result.final_output)


if __name__=='__main__':
 load_dotenv()
 asyncio.run(main())



