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
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")
slug = os.path.splitext(os.path.basename(HTML_FILE))[0]

page_url = f"{GITHUB_PAGES}/{os.path.basename(HTML_FILE)}"

title = ""

if soup.title:
    title = soup.title.text.strip()

description = ""

meta = soup.find("meta", attrs={"name": "description"})

if meta:
    description = meta.get("content", "").strip()

og_image = ""

meta = soup.find("meta", property="og:image")

if meta:
    og_image = meta.get("content", "").strip()

print("Title:", title)
print("Slug:", slug)
print("Description:", description)
print("Image:", og_image)
print("URL:", page_url)
url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items"

response = requests.get(url, headers=HEADERS)

response.raise_for_status()

items = response.json()["items"]
existing = None

for item in items:

    field_data = item.get("fieldData", {})

    if field_data.get("slug") == slug:
        existing = item
        break
        payload = {
    "isArchived": False,
    "isDraft": False,
    "fieldData": {
        "name": title,
        "slug": slug,
        "html-url": page_url
    }
}

if description:
    payload["fieldData"]["post-summary"] = description

if og_image:
    payload["fieldData"]["thumbnail-image"] = og_image
    if existing:

    item_id = existing["id"]

    print("Updating:", item_id)

    url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/{item_id}/live"

    response = requests.patch(
        url,
        headers=HEADERS,
        data=json.dumps(payload)
    )

else:

    print("Creating CMS Item")

    url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/live"

    response = requests.post(
        url,
        headers=HEADERS,
        data=json.dumps(payload)
    )

print(response.status_code)
print(response.text)
response.raise_for_status()

print("✅ Webflow synced successfully")
