from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Setup Chrome and WebDriver
options = webdriver.ChromeOptions()
options.headless = True  # Optional: Runs Chrome in headless mode.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Navigate to the Grafana dashboard
    driver.get('https://grafana.phys.ethz.ch/public-dashboards/59ac329ef03947d3836ac43a71db3c14')

    # Let's wait a few seconds to ensure the page has loaded. This time may need to be adjusted.
    driver.implicitly_wait(10)

    # Retrieve the page source
    html = driver.page_source

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Print the entire parsed HTML (optional: you can search for specific elements here)
    print(soup.prettify())

    print("new line")

finally:
    driver.quit()
