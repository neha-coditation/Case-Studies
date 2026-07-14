import os
import json
import requests

from bs4 import BeautifulSoup

WEBFLOW_TOKEN = os.environ["WEBFLOW_TOKEN"]
COLLECTION_ID = os.environ["COLLECTION_ID"]
GITHUB_PAGES = os.environ["GITHUB_PAGES"]

HEADERS = {
    "Authorization": f"Bearer {WEBFLOW_TOKEN}",
    "Content-Type": "application/json"
}

HTML_FILE = os.environ["HTML_FILE"]
