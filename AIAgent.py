from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('Gemini_api_key')


class InputModel(BaseModel):
    job_title: str
    location: str

class ResponseModel(BaseModel):
    Name: str
    Email_ID: str



input = InputModel(
    job_title= "Python Developer",
    location= "Canada"
)



model = GeminiModel('gemini-1.5-flash', api_key=api_key)
agent = Agent(  
    model = model,
    result_type=ResponseModel,
    system_prompt='Analyze queries crefully, Extract the name and email ID of the profile',  
)



def scrape_linkedin_profiles(job_title, location):
    # Write the code to scrape the profiles. The scraped data is represented in the profiles list below.

    profiles = [
        {"name": "Preethu", "title": "Python Developer", "location": "Canada", "email": "pree@gmail.com"},
        {"name": "Asha", "title": "React Developer", "location": "Canada", "email": "asha@gmail.com"}
    ]

    filtered_profiles = [
        profile for profile in profiles if profile['title'] == job_title and profile['location'] == location
    ]

    result = '. '.join(f"{profile['name']} is a {profile['title']} in {profile['location']}, their email ID is {profile['email']}" for profile in filtered_profiles)
    
    return result




result = agent.run_sync(scrape_linkedin_profiles(input.job_title, input.location))  

print(result.data.model_dump_json(indent=2))
