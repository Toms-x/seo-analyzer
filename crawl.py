import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# crawler configuration
starting_url = "https://www.tomintech.com/"

asset_folder = "tomintech_assets"

# helper function to download asset 

def download_asset(url, folder_path):
    # Skip if the URL is invalid or doesn't have a scheme
    if not url or not url.startswith(('http://', 'https://')):
        return

    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        # Get the filename from the URL
        filename = os.path.join(folder_path, url.split('/')[-1].split('?')[0])
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        # Save the file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  Downloaded: {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Could not download {url}: {e}")

# create asset folders
os.makedirs(asset_folder, exist_ok=True)
images_folder = os.path.join(asset_folder, "images")
css_folder = os.path.join(asset_folder, "css")
js_folder = os.path.join(asset_folder, "js")

# main crawler ---
urls_to_crawl = {starting_url} 
crawled_urls = set()

while urls_to_crawl and len(crawled_urls) < 50:
    current_url = urls_to_crawl.pop()
    if current_url in crawled_urls:
        continue

    print(f"\nCrawling: {current_url}")
    crawled_urls.add(current_url)
    
    try:
        response = requests.get(current_url, timeout=10)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. find and download CSS files
        for link_tag in soup.find_all('link', rel='stylesheet'):
            href = link_tag.get('href')
            absolute_url = urljoin(current_url, href)
            download_asset(absolute_url, css_folder)

        # 2. find and download javaScript files
        for script_tag in soup.find_all('script', src=True):
            src = script_tag.get('src')
            absolute_url = urljoin(current_url, src)
            download_asset(absolute_url, js_folder)

        # 3. find and download images
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            absolute_url = urljoin(current_url, src)
            download_asset(absolute_url, images_folder)

        # 4. find more pages to crawl
        for link_tag in soup.find_all('a'):
            href = link_tag.get('href')
            absolute_url = urljoin(current_url, href)
            if urlparse(starting_url).netloc == urlparse(absolute_url).netloc:
                if absolute_url not in crawled_urls and absolute_url not in urls_to_crawl:
                    urls_to_crawl.add(absolute_url)
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not crawl {current_url}: {e}")

print("\n✅ Asset download complete.")