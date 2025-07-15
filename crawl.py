import requests
from bs4 import BeautifulSoup

# my  website's homepage
homepage_url = "https://www.tomintech.com/"

print(f"Attempting to fetch {homepage_url}...")

try:
    response = requests.get(homepage_url, timeout=10)
    response.raise_for_status() 
    print(f"✅ Success! Status Code: {response.status_code}\n")

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a') # finds all the anchor tags <a> on the page

    print(f"Found {len(links)} total links on the page:")

# loops through the list of links and prints their 'href' attribute

    for link in links:
      print(link.get('href'))

except requests.exceptions.RequestException as e:
    print(f"❌ An error occurred: {e}")