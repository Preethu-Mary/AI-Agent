from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic import BaseModel
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
PHANTOM_ID = os.getenv('PHANTOM_ID')
LINKEDIN_COOKIE = os.getenv('LINKEDIN_COOKIE')

gemini_api_key = os.getenv('Gemini_api_key')


class InputModel(BaseModel):
    search: str
    category: str
    number_of_results: int

class ResponseModel(BaseModel):
    full_name: str
    first_name: str
    last_name: str
    job_title: str
    location: str
    company: str
    profile_url: str

input = InputModel(
    search= "React Developer",
    category= "People",
    number_of_results= 1
)



model = GeminiModel('gemini-1.5-flash', api_key=gemini_api_key)
agent = Agent(  
    model = model,
    result_type=ResponseModel,
    system_prompt='Extract all relevant information from the LinkedIn profile data.',  
)



# Function to start the Phantom
def start_phantom(search: str, category: str, number_of_results: int):
    url = f"https://api.phantombuster.com/api/v2/agents/launch"
    headers = {
        "Content-Type": "application/json",
        "X-Phantombuster-Key-1": API_KEY,
    }

    data = {
        "id":PHANTOM_ID,  
        "argument": {
            "sessionCookie": LINKEDIN_COOKIE,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "search": search,
            "category": category,
            "numberOfResultsPerLaunch": number_of_results,
            "numberOfResultsPerSearch": number_of_results,
        },
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Phantom started successfully!")
        return response.json()
    else:
        print("Error starting Phantom:", response.text)
        return None
    
def get_container_status(container_id):
    url = f"https://api.phantombuster.com/api/v2/containers/fetch?id={container_id}"

    headers = {
        "accept": "application/json",
        "X-Phantombuster-Key": API_KEY
    }

    response = requests.get(url, headers=headers)

    return response.json().get('status')

def get_result_object(container_id):
    # API endpoint to fetch Phantom details
    url = f"https://api.phantombuster.com/api/v2/containers/fetch-result-object?id={container_id}"

    headers = {
        "accept": "application/json",
        "X-Phantombuster-Key": API_KEY,
    }

    # Make the API call
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching Phantom results: {response.text}")
        return None


def scrape_linkedin_profiles(input: InputModel):
    # Write the code to scrape the profiles. The scraped data is represented in the profiles list below.

    import time
    # Start the Phantom
    phantom_data = start_phantom(input.search, input.category, input.number_of_results)
    container_id = phantom_data.get('containerId')
    print(container_id)

    while True:
        status = get_container_status(container_id)
        if status == "finished":
            print("Container Status is finished!")
            result = get_result_object(container_id).get('resultObject')
            return result
        time.sleep(1) 




result = agent.run_sync(scrape_linkedin_profiles(input))  

print(result.data.model_dump_json(indent=2))
