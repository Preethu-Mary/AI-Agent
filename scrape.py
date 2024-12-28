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
    url = f"https://api.phantombuster.com/api/v1/agent/{PHANTOM_ID}/launch"
    headers = {
        "Content-Type": "application/json",
        "X-Phantombuster-Key-1": API_KEY,
    }
    payload = {
        "argument": {
            "sessionCookie": LINKEDIN_COOKIE,
            "search": "elna",  # Specify your LinkedIn search query
            "numberOfResultsPerLaunch": 5,
            "numberOfResultsPerSearch": 5,
        },
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Phantom started successfully!")
        return response.json()
    else:
        print("Error starting Phantom:", response.text)
        return None

def get_result_file_url():
    # API endpoint to fetch Phantom details
    url = f"https://api.phantombuster.com/api/v2/agents/fetch"

    headers = {
        "X-Phantombuster-Key-1": API_KEY,
    }
    payload = {
        "id": PHANTOM_ID  # Provide the Phantom ID
    }

    # Make the API call
    response = requests.get(url, headers=headers, params=payload)

    if response.status_code == 200:
        
        # Extract s3Folder and orgS3Folder
        s3_folder = response.json().get("s3Folder")
        org_s3_folder = response.json().get("orgS3Folder")

        if s3_folder and org_s3_folder:
            # Construct the JSON and CSV URLs
            json_url = f"https://phantombuster.s3.amazonaws.com/{org_s3_folder}/{s3_folder}/result.json"
            csv_url = f"https://phantombuster.s3.amazonaws.com/{org_s3_folder}/{s3_folder}/result.csv"
            return {"JSON": json_url, "CSV": csv_url}
        else:
            print("Error: s3Folder or orgS3Folder not found in the response.")
            return None
    else:
        print(f"Error fetching Phantom details: {response.text}")
        return None

# Main Script
if __name__ == "__main__":
    # Start the Phantom
        phantom_data = start_phantom()
        
        # # Wait for Phantom to complete execution
        import time
        time.sleep(25)

        result_urls = get_result_file_url()
        if result_urls:
            print(f"JSON File: {result_urls['JSON']}")
        