import urllib.request

# Retrieve a random image of a cat from cataas.com
def getCatImage():
    url = "https://cataas.com/cat" 
    urllib.request.urlretrieve(url, "cat.jpeg")
