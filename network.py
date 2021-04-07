
import requests

URL = "http://mediametrics.ru/data/archive/day/ru-{}.zip"

def download_file(url, filename):
    r = requests.get(url, allow_redirects=True)
    if r.ok:
        open(filename, 'wb').write(r.content)
