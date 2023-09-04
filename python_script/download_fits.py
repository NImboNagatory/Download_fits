import os
import requests
from bs4 import BeautifulSoup


# Set the URL and destination directory
def create_dir_n_download_fits(url, destination):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination, exist_ok=True)

    # Send an HTTP GET request to the URL and parse the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links with ".fits" extension
    file_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.fits')]

    # Download each file to the destination directory
    for file_link in file_links:
        file_url = url + "/" + file_link
        local_path = os.path.join(destination, os.path.basename(file_link))

        # Download the file
        response = requests.get(file_url)
        with open(local_path, 'wb') as file:
            file.write(response.content)
