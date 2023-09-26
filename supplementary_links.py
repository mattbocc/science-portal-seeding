from selenium import webdriver

driver = webdriver.Firefox()

driver.get("https://doi.org/10.1249/MSS.0000000000002878")

links = driver.find_elements_by_tag_name("a")  # Find all <a> elements

for link in links:
    href = link.get_attribute("href")
    print(href)

driver.quit()
