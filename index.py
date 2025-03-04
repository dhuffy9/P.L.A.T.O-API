from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import requests

# Configure Edge options
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)  # Keep the browser open
options.set_capability("ms:loggingPrefs", {"performance": "ALL"})

# Initialize the driver
driver = webdriver.Edge(options=options)

# Enable Network monitoring
driver.execute_cdp_cmd("Network.enable", {})

# Go to the website and complete login flow
driver.get("https://learn.pct.edu/d2l/home")
wait = WebDriverWait(driver, 10)
login_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
login_button.click()

# Wait for page transition
wait.until(lambda driver: "microsoftonline.com" in driver.current_url or "learn.pct.edu" in driver.current_url)

print("Complete login if needed...")
time.sleep(2)  # Give time for login if needed

# Clear existing logs before navigating to work-to-do page
driver.get_log('performance')

# Now navigate to the work-to-do page
print("Navigating to work-to-do page and capturing API request URLs and headers...")
driver.get("https://learn.pct.edu/d2l/le/worktodo/view")

# Wait for page to load
time.sleep(2)

# Get all logs from this navigation
logs = driver.get_log('performance')

# Dictionary to store API request headers
api_headers = {}

# Collect all API request URLs and headers
for entry in logs:
    log = json.loads(entry["message"])["message"]
    
    if log.get("method") == "Network.requestWillBeSent":
        params = log.get("params", {})
        request = params.get("request", {})
        url = request.get("url")
        headers = request.get("headers", {})
        
        if url and ("api" in url.lower() or url.endswith((".json", ".xml"))):
            api_headers[url] = headers

# Print collected API URLs and their headers
print("\n--- API REQUEST URLs and HEADERS ---\n")
for url, headers in api_headers.items():
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}\n")


# Dictionary to store organized request data
request_data = {}

# Define valid URL patterns to look for
valid_urls = ["organizations", "assignments", "quizzes"]

# Process each API URL
for url in api_headers:
    # Skip URLs containing "notifications"
    if "notifications" in url:
        continue
        
    # Check if URL contains any of our valid patterns
    for valid_url_type in valid_urls:
        if valid_url_type in url:
            print(f"Found relevant URL: {url}")
            
            # Handle organization (class) URLs
            if valid_url_type == valid_urls[0]:  # "organizations"
                # Extract class name from URL or response if possible
                # For now, use the URL as the key
                class_key = url
                request_data[class_key] = {"assignments": [], "quizzes": []}
            
            # Handle assignment URLs
            elif valid_url_type == valid_urls[1]:  # "assignments"
                class_code = url.split("/")[-3]  # Extract class code from URL
                
                # Find the corresponding class URL and add this assignment
                for class_url in request_data:
                    if class_code in class_url:
                        request_data[class_url]["assignments"].append(url)
                        break
            
            # Handle quiz URLs
            elif valid_url_type == valid_urls[2]:  # "quizzes"
                class_code = url.split("/")[-3]  # Extract class code from URL
                
                # Find the corresponding class URL and add this quiz
                for class_url in request_data:
                    if class_code in class_url:
                        request_data[class_url]["quizzes"].append(url)
                        break
                
            # Once we've matched a URL type, no need to check other types
            break

# Print the organized data structure
print("\n--- ORGANIZED CLASS DATA ---\n")
for class_url, data in request_data.items():
    print(f"Class URL: {class_url}")
    print(f"Assignments: {len(data['assignments'])}")
    print(f"Quizzes: {len(data['quizzes'])}")
    print()

# Now fetch actual data for each class
for class_url, data in request_data.items():
    print(f"\nProcessing class: {class_url}")
    
    # Create a session with cookies
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
    
    # Fetch and process assignments
    for assignment_url in data["assignments"]:
        try:
            response = session.get(assignment_url, headers=api_headers.get(assignment_url, {}))
            if response.status_code == 200:
                assignment_data = response.json()
                print(f"Successfully retrieved assignment data from {assignment_url}")
                # Process assignment data as needed
            else:
                print(f"Failed to retrieve assignment data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching assignment data: {str(e)}")
    
    # Fetch and process quizzes
    for quiz_url in data["quizzes"]:
        try:
            response = session.get(quiz_url, headers=api_headers.get(quiz_url, {}))
            if response.status_code == 200:
                quiz_data = response.json()
                print(f"Successfully retrieved quiz data from {quiz_url}")
                # Process quiz data as needed
            else:
                print(f"Failed to retrieve quiz data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching quiz data: {str(e)}")

# Testing data #
# url = "https://67f8200b-dc2a-4854-aa97-0555dd5c5121.assignments.api.brightspace.com/93801/folders/272110"
# try:
#     # Get cookies from selenium session
#     selenium_cookies = driver.get_cookies()
    
#     # Create a session object and add cookies
#     session = requests.Session()
#     for cookie in selenium_cookies:
#         session.cookies.set(cookie['name'], cookie['value'])
    
#     # Make the request using the session with cookies and headers
#     response = session.get(url, headers=api_headers[url])
#     if response.status_code == 200:
#         data = response.json()
#         print(f"Successfully retrieved data from {url}")
#         print(json.dumps(data, indent=2))
#     else:
#         print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
# except Exception as e:
#     print(f"Error making request to {url}: {str(e)}")

