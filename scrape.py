import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
PHANTOM_ID = os.getenv('PHANTOM_ID')
LINKEDIN_COOKIE = os.getenv('LINKEDIN_COOKIE')

# Function to start the Phantom
def start_phantom():
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
            "search": "KPMG",
            "category": "Companies",
            "numberOfResultsPerLaunch": 1,
            "numberOfResultsPerSearch": 1,
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
        # Extract s3Folder and orgS3Folder
        # s3_folder = response.json().get("s3Folder")
        # org_s3_folder = response.json().get("orgS3Folder")

        # if s3_folder and org_s3_folder:
        #     # Construct the JSON and CSV URLs
        #     json_url = f"https://phantombuster.s3.amazonaws.com/{org_s3_folder}/{s3_folder}/result.csv"
        #     return {"JSON": json_url}
        # else:
        #     print("Error: s3Folder or orgS3Folder not found in the response.")
        #     return None
    else:
        print(f"Error fetching Phantom results: {response.text}")
        return None

# Main Script
if __name__ == "__main__":
        import time
    # Start the Phantom
        phantom_data = start_phantom()
        container_id = phantom_data.get('containerId')
        print(container_id)

        while True:
            status = get_container_status(container_id)
            if status == "finished":
                print("Container Status is finished!")
                result = get_result_object(container_id).get('resultObject')
                print(result)
                break
            time.sleep(1) 
    
        