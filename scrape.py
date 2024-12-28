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
            "search": "Mary george",  # Specify your LinkedIn search query
            "numberOfResultsPerLaunch": 5,
            "numberOfResultsPerSearch": 5,
        },
    }
    
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    
    if response.status_code == 200:
        print("Phantom started successfully!")
        return response.json()
    else:
        print("Error starting Phantom:", response.text)
        return None

# Function to retrieve the results
def get_results(container_id):
    url = f"https://api.phantombuster.com/api/v1/agent/{PHANTOM_ID}/output?containerId={container_id}"
    headers = {
        "X-Phantombuster-Key-1": API_KEY,
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Results retrieved successfully!")
        return response.json()
    else:
        print("Error retrieving results:", response.text)
        return None

# Main Script
if __name__ == "__main__":
    # Start the Phantom
    phantom_data = start_phantom()
    
    if phantom_data:
        container_id = phantom_data.get("data", {}).get("containerId")
        if container_id:
            print("Container ID:", container_id)
        else:
            print("containerId not found in the response")
        
        # Wait for Phantom to complete execution
        import time
        time.sleep(5)  # Adjust based on Phantom's estimated run time
        
        # Fetch the results
        results = get_results(container_id)
        time.sleep(5)
        
        # Save or display the results
        if results:
            with open("linkedin_results.json", "w") as file:
                json.dump(results, file, indent=4)
            print("Results saved to linkedin_results.json")
