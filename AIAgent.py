from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic import BaseModel
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY') # PhantomBuster API Key
PHANTOM_ID = os.getenv('PHANTOM_ID')
LINKEDIN_COOKIE = os.getenv('LINKEDIN_COOKIE')

gemini_api_key = os.getenv('Gemini_api_key')


class InputModel(BaseModel):
    search: str
    category: str
    number_of_results: int

class ResponseItemModel(BaseModel):
    full_name: str
    first_name: str
    last_name: str
    job_title: str
    additionalInfo: str
    location: str
    company: str
    Industry: str
    profile_url: str
    profileImageUrl: str

class ResponseModel(BaseModel):
    results: list[ResponseItemModel]

input = InputModel(
    search= "Python Developer, Canada",
    category= "People",
    number_of_results= 2
)

model = GeminiModel('gemini-1.5-flash', api_key=gemini_api_key)
agent = Agent(  
    model = model,
    result_type=ResponseModel,
    system_prompt='Extract all relevant information from the LinkedIn profile data not just one all of them. if there is no linkedin profile data, provide empty strings',  
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

def get_results_all_csv():
    url = f"https://api.phantombuster.com/api/v2/agents/fetch?id={PHANTOM_ID}"

    headers = {
        "accept": "application/json",
        "X-Phantombuster-Key": API_KEY,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Extract s3Folder and orgS3Folder
        s3_folder = response.json().get("s3Folder")
        org_s3_folder = response.json().get("orgS3Folder")

        if s3_folder and org_s3_folder:
            # Construct the JSON and CSV URLs
            csv_url = f"https://phantombuster.s3.amazonaws.com/{org_s3_folder}/{s3_folder}/result.csv"
            return csv_url
        else:
            print("Error: s3Folder or orgS3Folder not found in the response.")
            return None
    else:
        print(f"Error fetching Phantom results: {response.text}")
        return None

def scrape_linkedin_profiles(input: InputModel):
    import time
    # Start the Phantom
    phantom_data = start_phantom(input.search, input.category, input.number_of_results)
    container_id = phantom_data.get('containerId')
    print(container_id)

    while True:
        status = get_container_status(container_id)
        if status == "finished":
            print("Container Status is finished!")
            print(f"Query: {input}")
            result = get_result_object(container_id).get('resultObject')
            csv = get_results_all_csv()
            if result:
                return result
            else:
                print(f"Results: Results are none or those results may have already been retrieved. \nPLEASE SEE THE CSV FILE TO VIEW ALL THE PAST RESULTS THAT HAS BEEN FETCHED SO FAR! \n CSV: {csv}")
                return ""
        time.sleep(1) 

result = agent.run_sync(scrape_linkedin_profiles(input))  

print(result.data.model_dump_json(indent=2))
