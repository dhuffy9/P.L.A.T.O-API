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


# Clear all types of storage before starting
driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
    "origin": "*",
    "storageTypes": "all"
})

# Delete all cookies
driver.delete_all_cookies()

# Go to the website and wait for the page to load
driver.get("https://learn.pct.edu/d2l/home")
wait = WebDriverWait(driver, 10)  # Create a wait object with 10 second timeout
# Wait for the button to be clickable
login_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
login_button.click()

# Wait for the page transition
wait.until(lambda driver: "microsoftonline.com" in driver.current_url or "learn.pct.edu" in driver.current_url)

if "https://login.microsoftonline.com" in driver.current_url:
    print("User has not yet been logged in, logging in.....")
    # Wait for username input to be present
    username_input = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    print(username_input)
    username_input.send_keys(username)
    # Find all inputs and click the enter button
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(inputs)

    inputs[2].click()
else:
    print("User already loged in, getting data")
    driver.get("https://learn.pct.edu/d2l/le/worktodo/view")
    



# fetch('https://67f8200b-dc2a-4854-aa97-0555dd5c5121.activities.api.brightspace.com/users/66056?start=2025-02-25T05%3a33%3a41.041Z&end=2025-03-04T05%3a33%3a41.041Z&activeCoursesOnly=1', {
#   method: 'GET',
#   headers: {
#     'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImNkYTlhMjQ5LTU4MWMtNGE2MC1hZmRjLWE4OGQwZWI3YWFjZCIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NDA0NjA5NjksImV4cCI6MTc0MDQ2NDU2OSwiaXNzIjoiaHR0cHM6Ly9hcGkuYnJpZ2h0c3BhY2UuY29tL2F1dGgiLCJhdWQiOiJodHRwczovL2FwaS5icmlnaHRzcGFjZS5jb20vYXV0aC90b2tlbiIsInRlbmFudGlkIjoiNjdmODIwMGItZGMyYS00ODU0LWFhOTctMDU1NWRkNWM1MTIxIiwic3ViIjoiNjYwNTYiLCJhenAiOiJkMmwtaWFtLWxtcyIsInNjb3BlIjoiKjoqOioiLCJqdGkiOiI5Y2E1MjkyYy04NmYxLTQ3ZTYtYmI4ZC05MjM3NWZhMjViZGMifQ.vl1OQzXKL2fR7_-vfI4GNoVJhqJ8lTDjhIMu5k8iz-u7Sg2Gw6NDycww8p9tOL5XdF95l1gBAFQvsCZMLfnDqd0lqxzuCWaQpdvwSzeOlg_gcGmWX0LTnqo8Q6kk3pSj6_ltYzjsauJtJ7KhRaRr3pGAVaTWjrKcDH8b1-hppac1R3sz1DjPdDbOj6tFFOs5dTCH-XdT_yAf-bp8nhkuAEh0f8eVHYMKyXuMrf2kHYdRsjGDF66XOjsNqc9v93uEGOEwM8eHbf2OyBnX4sV7XXax0ZACk3t1mxR3ijYOYsRvhfKn0kxYBFE64EZLJa83EQmBA4RuBPEtlaEEEXQhJA', // Replace with your actual token if it's not current
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Accept-Language': 'en-US,en;q=0.9',
#   }
# })
#   .then(response => {
#     if (!response.ok) {
#       throw new Error('Network response was not ok');
#     }
#     return response.json();
#   })
#   .then(data => {
#     console.log('Data retrieved successfully:', data);
#   })
#   .catch(error => {
#     console.error('Failed to retrieve data:', error);
#   });


# // First, fetch the list of assignments
# fetch('https://67f8200b-dc2a-4854-aa97-0555dd5c5121.activities.api.brightspace.com/users/66056?start=2025-02-25T05%3a33%3a41.041Z&end=2025-03-04T05%3a33%3a41.041Z&activeCoursesOnly=1', {
#   method: 'GET',
#   headers: {
#     'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImNkYTlhMjQ5LTU4MWMtNGE2MC1hZmRjLWE4OGQwZWI3YWFjZCIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NDA0NjA5NjksImV4cCI6MTc0MDQ2NDU2OSwiaXNzIjoiaHR0cHM6Ly9hcGkuYnJpZ2h0c3BhY2UuY29tL2F1dGgiLCJhdWQiOiJodHRwczovL2FwaS5icmlnaHRzcGFjZS5jb20vYXV0aC90b2tlbiIsInRlbmFudGlkIjoiNjdmODIwMGItZGMyYS00ODU0LWFhOTctMDU1NWRkNWM1MTIxIiwic3ViIjoiNjYwNTYiLCJhenAiOiJkMmwtaWFtLWxtcyIsInNjb3BlIjoiKjoqOioiLCJqdGkiOiI5Y2E1MjkyYy04NmYxLTQ3ZTYtYmI4ZC05MjM3NWZhMjViZGMifQ.vl1OQzXKL2fR7_-vfI4GNoVJhqJ8lTDjhIMu5k8iz-u7Sg2Gw6NDycww8p9tOL5XdF95l1gBAFQvsCZMLfnDqd0lqxzuCWaQpdvwSzeOlg_gcGmWX0LTnqo8Q6kk3pSj6_ltYzjsauJtJ7KhRaRr3pGAVaTWjrKcDH8b1-hppac1R3sz1DjPdDbOj6tFFOs5dTCH-XdT_yAf-bp8nhkuAEh0f8eVHYMKyXuMrf2kHYdRsjGDF66XOjsNqc9v93uEGOEwM8eHbf2OyBnX4sV7XXax0ZACk3t1mxR3ijYOYsRvhfKn0kxYBFE64EZLJa83EQmBA4RuBPEtlaEEEXQhJA',
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Accept-Language': 'en-US,en;q=0.9',
#   }
# })
# .then(response => {
#   if (!response.ok) {
#     throw new Error('Network response was not ok');
#   }
#   return response.json();
# })
# .then(data => {
#   console.log('Assignment list retrieved successfully:', data);
  
#   // Extract assignment URLs from the list
#   const assignmentLinks = data.entities.map(assignment => {
#     const assignmentLink = assignment.links.find(link => 
#       link.rel && link.rel.includes("https://api.brightspace.com/rels/assignment")
#     );
    
#     if (assignmentLink) {
#       return {
#         url: assignmentLink.href,
#         id: assignment.links.find(link => 
#           link.rel && link.rel.includes("self")
#         )?.href.split('/').pop()
#       };
#     }
#     return null;
#   }).filter(link => link !== null);
  
#   // Fetch details for each assignment
#   return Promise.all(assignmentLinks.map(link => 
#     fetchAssignmentDetails(link.url)
#   ));
# })
# .then(detailedAssignments => {
#   console.log('All assignment details retrieved:', detailedAssignments);
# })
# .catch(error => {
#   console.error('Failed to retrieve data:', error);
# });

# // Function to fetch details for a specific assignment
# function fetchAssignmentDetails(url) {
#   return fetch(url, {
#     method: 'GET',
#     headers: {
#       'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImNkYTlhMjQ5LTU4MWMtNGE2MC1hZmRjLWE4OGQwZWI3YWFjZCIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NDA0NjA5NjksImV4cCI6MTc0MDQ2NDU2OSwiaXNzIjoiaHR0cHM6Ly9hcGkuYnJpZ2h0c3BhY2UuY29tL2F1dGgiLCJhdWQiOiJodHRwczovL2FwaS5icmlnaHRzcGFjZS5jb20vYXV0aC90b2tlbiIsInRlbmFudGlkIjoiNjdmODIwMGItZGMyYS00ODU0LWFhOTctMDU1NWRkNWM1MTIxIiwic3ViIjoiNjYwNTYiLCJhenAiOiJkMmwtaWFtLWxtcyIsInNjb3BlIjoiKjoqOioiLCJqdGkiOiI5Y2E1MjkyYy04NmYxLTQ3ZTYtYmI4ZC05MjM3NWZhMjViZGMifQ.vl1OQzXKL2fR7_-vfI4GNoVJhqJ8lTDjhIMu5k8iz-u7Sg2Gw6NDycww8p9tOL5XdF95l1gBAFQvsCZMLfnDqd0lqxzuCWaQpdvwSzeOlg_gcGmWX0LTnqo8Q6kk3pSj6_ltYzjsauJtJ7KhRaRr3pGAVaTWjrKcDH8b1-hppac1R3sz1DjPdDbOj6tFFOs5dTCH-XdT_yAf-bp8nhkuAEh0f8eVHYMKyXuMrf2kHYdRsjGDF66XOjsNqc9v93uEGOEwM8eHbf2OyBnX4sV7XXax0ZACk3t1mxR3ijYOYsRvhfKn0kxYBFE64EZLJa83EQmBA4RuBPEtlaEEEXQhJA',
#       'Accept': '*/*',
#       'Accept-Encoding': 'gzip, deflate, br, zstd',
#       'Accept-Language': 'en-US,en;q=0.9',
#     }
#   })
#   .then(response => {
#     if (!response.ok) {
#       throw new Error(`Network response was not ok for assignment: ${url}`);
#     }
#     return response.json();
#   })
#   .then(assignmentData => {
#     console.log(`Details for assignment at ${url}:`, assignmentData);
#     return {
#       url: url,
#       details: assignmentData
#     };
#   })
#   .catch(error => {
#     console.error(`Failed to retrieve details for assignment ${url}:`, error);
#     return {
#       url: url,
#       error: error.message
#     };
#   });
# }
