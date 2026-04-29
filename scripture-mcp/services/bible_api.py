 # Calls helloao API
import requests

BASE_URL = "https://bible.helloao.org/api"

def get_books(translation="BSB"):
    url = f"{BASE_URL}/{translation}/books.json"
    return requests.get(url).json()

def get_chapter(translation, book, chapter):
    url = f"{BASE_URL}/{translation}/{book}/{chapter}.json"
    return requests.get(url).json()