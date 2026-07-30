import asyncio
from dotenv import load_dotenv
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




if __name__=='__main__':
    load_dotenv()
    asyncio.run(main())