from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Create a browser instance with options to prevent automatic closing
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)  # This keeps the browser open
driver = webdriver.Edge(options=options)

# Go to the website and wait for the page to load
driver.get("https://learn.pct.edu/d2l/home")
wait = WebDriverWait(driver, 10)  # Create a wait object with 10 second timeout
# Wait for the button to be clickable
login_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
login_button.click()

# Wait for the page transition
wait.until(EC.url_contains("microsoftonline.com") or EC.url_contains("learn.pct.edu"))

if driver.current_url[:34] == "https://login.microsoftonline.com/":
    print("User has not yet been logged in, logging in.....")
    # Wait for username input to be present
    username_input = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input"))  )
    username_input.send_keys(username)
    # Find all inputs and click the enter button
    inputs = driver.find_elements(By.TAG_NAME, "input")
    inputs[2].click()
else:
    print("User already loged in, getting data")
    driver.get("https://learn.pct.edu/d2l/le/worktodo/view")
    



# Find all work items
# work_items = driver.find_elements(By.CSS_SELECTOR, "d2l-w2d-work-item")

# # Extract and print information for each work item
# for item in work_items:
#     try:
#         title = item.get_attribute("text")
#         due_date = item.get_attribute("due-date")
#         course = item.get_attribute("organization-name")
        
#         print(f"Assignment: {title}")
#         print(f"Due Date: {due_date}")
#         print(f"Course: {course}")
#         print("-" * 50)
#     except Exception as e:
#         print(f"Error extracting item information: {e}")

# # Find and click the search button
# driver.find_elements(By.TAG_NAME, "textarea")
# search_button = driver.find_element(By.NAME, "btnK")
# search_button.click()