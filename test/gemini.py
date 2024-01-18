from dotenv import load_dotenv
import json
load_dotenv()
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name='gemini-pro')

from datetime import date, timedelta
today = str(date.today()).split("-")
today = today[2] + "-" + today[1] + "-" + today[0]
after_three_days = str(date.today() + timedelta(days=3)).split("-")
after_three_days = after_three_days[2] + "-" + after_three_days[1] + "-" + after_three_days[0]
start_date = today
end_date = after_three_days
destination = "Paris"
prompt = """Consider yourself a travel planner. Show me day wise planner for all days from """ + str(
                    start_date) + """ to """ + str(end_date) + """Display the output in form of valid JSON object:
                        { "introduction": "Give brief description about """ + str(destination) + """ ",
                         "itinerary": 
                            [
                                { 
                                    "Day": "Day number follow format as 1" ,
                                    "morning": "suggest popular restaurants to have breakfast, suggest places of interest, commute to places" ,
                                    "afternoon": "suggest popular restaurants to have lunch, suggest places of interest, commute to places"  ,
                                    "evening": "suggest popular restaurants to have snacks and party, suggest places of interest, commute to places" ,
                                    "night": "suggest popular restaurants to have dinner, suggest places of interest, commute to places"
                                }
                            ] 
                        }"""
response = model.generate_content(prompt)
print(response.text)
print(json.loads(response.text[3:-3]))