import json
import os
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Load the JSON file containing the list of unique journal names
with open('unique_journals.json', 'r') as f:
    unique_journals = json.load(f)

# Directory to store downloaded images
output_directory = 'journal_images'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Dictionary to store journal names and their corresponding image paths
journal_images = {}

# Initialize the Selenium web driver (ensure you have the appropriate web driver executable in your PATH)
driver = webdriver.Chrome()  # Use appropriate driver based on your browser

# Iterate through the list of unique journal names
for journal in unique_journals:
    # Replace spaces with underscores in the journal name for the filename
    filename = journal.replace(" ", "_")

    # Search for the journal's cover image
    driver.get("https://www.google.com/imghp")
    search_box = driver.find_element_by_name("q")
    search_box.send_keys(f"{journal} journal cover")
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(random(10, 30))

    # Find the first image element and download it
    images = driver.find_elements_by_css_selector("img.rg_i")
    if images:
        img_url = images[0].get_attribute('src')
        if img_url:
            image_path = f"{output_directory}/{filename}.jpg"
            with open(image_path, 'wb') as f:
                f.write(requests.get(img_url).content)
            journal_images[journal] = image_path
        else:
            print(f"No image found for {journal}.")
    else:
        print(f"No image found for {journal}.")

# Save the dictionary to a JSON file
with open('journal_images_selenium.json', 'w') as f:
    json.dump(journal_images, f, indent=4)

# Close the Selenium web driver
driver.quit()

print("Journal images have been downloaded and saved to journal_images_selenium.json.")
