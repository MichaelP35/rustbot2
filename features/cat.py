import urllib.request
from concurrent.futures import ThreadPoolExecutor


# Retrieves file from a url
def download_cat_image(url, filename):
    urllib.request.urlretrieve(url, filename)


# Retrieves images concurrently
def getCatImage(num: int):
    url = "https://cataas.com/cat"
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_cat_image, url, f"images/cat{i}.jpeg") for i in range(num)]
        for future in futures:
            future.result()  # Wait for each download to complete
