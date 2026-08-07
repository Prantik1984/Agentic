import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner,trace,function_tool
import os
from Operators.db_operator import DBOperator

dboperator = DBOperator()

@function_tool
def calorie_lookup_tool(query: str) -> str:
    """
    Look up calorie information for a single food item.

    Args:
        query: The food item to look up.

    Returns:
        Matching nutrition information per 100 grams.
    """
    return dboperator.Query_DB(
        query=query
    )

async def main():
   open_ai_key=os.getenv('OPENAI_API_KEY')

   food_option=input("What do you want to have for breakfast? ")
   while food_option==None or food_option=='':
       print("Type in a valid item")
       food_option = input("What do you want to have for breakfast? ")


   while True:
       breakfast_choice_count = input("How many options do you want to breakfast? ")
       try:
           breakfast_choice_count = int(breakfast_choice_count)
           break
       except ValueError:
           print("Enter a valid number")

   while True:
       breakfast_calories_count = input("How many calories do you want to breakfast? ")
       try:
           breakfast_calories_count = int(breakfast_calories_count)
           break
       except ValueError:
           print("Enter a valid number")

   lookup = dboperator.Query_DB(food_option)
   print(lookup)
   return

   instructions = f"""
       * You are a breakfast advisor. You come up with meal plans for the user based on their preferences.
       * You also calculate the calories for the meal and its ingredients.
       * Create {breakfast_choice_count} breakfast plans for the user. For each meal, give a name, the ingredients, and the calories
       * The calories should be equal or just around the {breakfast_calories_count}
       * The breakfast plans should include {food_option}
       * If you need to look up calorie information, use the calorie_lookup_tool.
       * If the {food_option} cannot be found using the calorie_lookup_tool.Say that could not find relevant data
       * Do not make up things 
       """

   with trace("Breakfast planner agent"):
       nutrition_agent = Agent(
           name="Breakfast_Planner_Agent",
           instructions=instructions,
           tools=[calorie_lookup_tool],
       )

       query = "Create a breakfast plan"

       result = await Runner.run(nutrition_agent, query)
       print(result.final_output)


if __name__=='__main__':
    load_dotenv()
    asyncio.run(main())