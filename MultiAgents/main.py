import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner,trace
import os
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

   instructions = f"""
       * You are a breakfast advisor. You come up with meal plans for the user based on their preferences.
       * You also calculate the calories for the meal and its ingredients.
       * Create {breakfast_choice_count} breakfast plans for the user. For each meal, give a name, the ingredients, and the calories
       * The calories should be equal or just around the {breakfast_calories_count}
       * The breakfast plans should include {food_option}
       """

   with trace("Breakfast planner agent"):
       nutrition_agent = Agent(
           name="Breakfast_Planner_Agent",
           instructions=instructions,
       )

       query = "Create a breakfast plan"

       result = await Runner.run(nutrition_agent, query)
       print(result.final_output)


if __name__=='__main__':
    load_dotenv()
    asyncio.run(main())