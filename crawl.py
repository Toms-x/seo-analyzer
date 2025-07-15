import requests

# my  website's homepage
homepage_url = "https://www.tomintech.com/"

print(f"Attempting to fetch {homepage_url}...")

try:
    response = requests.get(homepage_url, timeout=10)
    response.raise_for_status() 
    print(f"✅ Success! Status Code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"❌ An error occurred: {e}")
