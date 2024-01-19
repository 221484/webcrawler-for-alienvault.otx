import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_all_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.217 Safari/537.37"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith('http')]
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching links: {e}")
        return []

def get_all_ips(url):
    driver = None

    try:
        chrome_options = Options()
        # (Your existing Chrome options here)

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # (Your existing code for waiting and handling the JavaScript execution)

        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', driver.page_source)
        return ips
    except Exception as e:
        print(f"Error getting IPs: {e}")
        return []
    finally:
        if driver:
            driver.quit()

def web_crawler(base_url, max_pages):
    visited = set()
    pages_to_visit = {base_url}
    
    while pages_to_visit and len(visited) < max_pages:
        current_page = pages_to_visit.pop()
        visited.add(current_page)
        print("Visited:", current_page)

        try:
            new_links = set(get_all_links(current_page)) - visited
            pages_to_visit.update(new_links)
        except Exception as e:
            print(f"Error processing links on {current_page}: {e}")

    all_ips = []
    for page in visited:
        all_ips.extend(get_all_ips(page))

    return all_ips

if __name__ == "__main__":
    base_url = input("Enter the base URL: ")
    try:
        all_ips = web_crawler(base_url, 50)
        print("Unique IPs:")
        for ip in set(all_ips):
            print(ip)
    except Exception as e:
        print(f"Error: {e}")