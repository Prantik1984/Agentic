import asyncio
from turtledemo.paint import switchupdown

from dotenv import load_dotenv

from Utilities.DbOperator import DBOperator
from agents import Agent,trace,Runner,function_tool

db_operator = DBOperator()
@function_tool
def calorie_lookup_tool(query: str) -> str:
    """
    Look up calorie information for a single food item.

    Args:
        query: The food item to look up.

    Returns:
        Matching nutrition information per 100 grams.
    """
    return db_operator.Query_CSV_DB(
        query=query,
        db_path="../ChromaDB",
    )

async def main():
    prompt=""""
    What do you want to do?
    Press 1 to create the chroma db
    Press 2 to ask a question
    """
    answer=input(prompt)

    match answer:
        case "1":
            db_operator.Create_CSV_DB("../ChromaDB","./data/calories.csv")
        case "2":
            query=input("What do you want to know about nutrition?")
            calorie_agent = Agent(
                name="Nutrition Assistant",
                instructions="""
                You are a helpful nutrition assistant giving out calorie information.
    You give concise answers.
    If you need to look up calorie information, use the calorie_lookup_tool.
    If you donot find any information, say that information about this is unavailable
                """,
                tools=[calorie_lookup_tool],
            )
            with trace("Nutrition Assistant with RAG"):
                result = await Runner.run(
                    calorie_agent,
                    query,
                )
                print(result.final_output)
            # db_operator.Query_CSV_DB(query,"../ChromaDB")

if __name__=='__main__':
    load_dotenv()
    asyncio.run(main())