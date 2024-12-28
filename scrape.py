import requests
import json

# PhantomBuster API Key
API_KEY = "OsdABgNzMKROxkYGLphQsYkTerXeMi5lbFX12kjRezg"

# LinkedIn Profile Scraper Phantom ID
PHANTOM_ID = "4161056667274732"  # Get this from the Phantom's settings page

# LinkedIn Session Cookie (li_at)
LINKEDIN_COOKIE = "AQEDAShUJNAEIcfSAAABlAsV6Z4AAAGULyJtnlYAUnN9gLs0cP0wJUYfed5g9t9IntwtLg9pXgDILd5DVkSwDz-JW4V2M6bfjRVjNH5Dh-pB-v5wCNQ6mXHX__IJFqNKqL_g3Bo3Ru17N6qU_NNyRHrc"

# # Function to start the Phantom
# def start_phantom():
#     url = f"https://api.phantombuster.com/api/v1/agent/{PHANTOM_ID}/launch"
#     headers = {
#         "Content-Type": "application/json",
#         "X-Phantombuster-Key-1": API_KEY,
#     }
#     payload = {
#         "argument": {
#             "sessionCookie": LINKEDIN_COOKIE,
#             "search": "Mary george",  # Specify your LinkedIn search query
#             "numberOfResultsPerLaunch": 5,
#             "numberOfResultsPerSearch": 5,
#         },
#     }
    
#     response = requests.post(url, headers=headers, json=payload)
#     print(response.json())
    
#     if response.status_code == 200:
#         print("Phantom started successfully!")
#         return response.json()
#     else:
#         print("Error starting Phantom:", response.text)
#         return None

# # Function to retrieve the results
# def get_results(container_id):
#     url = f"https://api.phantombuster.com/api/v1/agent/{PHANTOM_ID}/output?containerId={container_id}"
#     headers = {
#         "X-Phantombuster-Key-1": API_KEY,
#     }
    
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         print("Results retrieved successfully!")
#         return response.json()
#     else:
#         print("Error retrieving results:", response.text)
#         return None

# # Main Script
# if __name__ == "__main__":
#     # Start the Phantom
#     phantom_data = start_phantom()
    
#     if phantom_data:
#         container_id = phantom_data.get("data", {}).get("containerId")
#         if container_id:
#             print("Container ID:", container_id)
#         else:
#             print("containerId not found in the response")
        
#         # Wait for Phantom to complete execution
#         import time
#         time.sleep(5)  # Adjust based on Phantom's estimated run time
        
#         # Fetch the results
#         results = get_results(container_id)
#         time.sleep(5)
        
#         # Save or display the results
#         if results:
#             with open("linkedin_results.json", "w") as file:
#                 json.dump(results, file, indent=4)
#             print("Results saved to linkedin_results.json")


LIST_ID = "6280954548252470"  # Replace with the actual List ID

# API URL to export data as a file
url = f"https://api.phantombuster.com/api/v2/org-storage/lists/{LIST_ID}/data/export"

# Set headers for authentication
headers = {
    "X-Phantombuster-Key-1": API_KEY,
}

# Make the GET request to download the file
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Save the content to a CSV file
    with open("scraped_profiles.csv", "wb") as file:
        file.write(response.content)
    print("Profiles saved to scraped_profiles.csv")
else:
    print("Error downloading profiles:", response.text)

