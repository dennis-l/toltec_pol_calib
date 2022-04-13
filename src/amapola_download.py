import os
import requests

def download_file(url, destination):
    """ Download file
    https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    """
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(destination, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return destination

if __name__ == "__main__":
    amapola_url = 'http://www.alma.cl/~skameno/AMAPOLA/amapola.txt'
    download_file(amapola_url, 'data/amapola.txt')