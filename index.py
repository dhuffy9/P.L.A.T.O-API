from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create a browser instance with options to prevent automatic closing
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)  # This keeps the browser open
driver = webdriver.Edge(options=options)

# Go to the website and wait for the page to loadWS
driver.get("https://learn.pct.edu/d2l/home")
time.sleep(1)

# Find the penn college account button and click
search_box = driver.find_elements(By.TAG_NAME, "button")[0]
search_box.click()

# wait for the page to load
time.sleep(1)

if driver.current_url[:34] == "https://login.microsoftonline.com/":
    inputs = driver.find_elements(By.TAG_NAME, "input")
    username_input = inputs[0].send_keys("djh61@pct.edu")
    enter_button =  inputs[2].click()

# Wait for the work-to-do widget to be present
wait = WebDriverWait(driver, 10)
work_to_do = wait.until(EC.presence_of_element_located((By.TAG_NAME, "d2l-w2d-work-to-do")))

# Find all work items
work_items = driver.find_elements(By.CSS_SELECTOR, "d2l-w2d-work-item")

# Extract and print information for each work item
for item in work_items:
    try:
        title = item.get_attribute("text")
        due_date = item.get_attribute("due-date")
        course = item.get_attribute("organization-name")
        
        print(f"Assignment: {title}")
        print(f"Due Date: {due_date}")
        print(f"Course: {course}")
        print("-" * 50)
    except Exception as e:
        print(f"Error extracting item information: {e}")

# # Find and click the search button
# driver.find_elements(By.TAG_NAME, "textarea")
# search_button = driver.find_element(By.NAME, "btnK")
# search_button.click()