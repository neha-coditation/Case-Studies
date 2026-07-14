import os
import json
import requests
from bs4 import BeautifulSoup

WEBFLOW_TOKEN = os.environ["WEBFLOW_TOKEN"]
COLLECTION_ID = os.environ["COLLECTION_ID"]
GITHUB_PAGES = os.environ["GITHUB_PAGES"]
HTML_FILE = os.environ["HTML_FILE"]

HEADERS = {
    "Authorization": f"Bearer {WEBFLOW_TOKEN}",
    "Content-Type": "application/json"
}

# Read HTML
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

slug = os.path.splitext(os.path.basename(HTML_FILE))[0]
page_url = f"{GITHUB_PAGES}/{os.path.basename(HTML_FILE)}"

# Title
title = ""

if soup.title:
    title = soup.title.text.strip()

if not title:
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)

if not title:
    title = slug.replace("-", " ").title()

# Description
description = ""

meta = (
    soup.find("meta", attrs={"name": "description"})
    or soup.find("meta", attrs={"property": "og:description"})
)

if meta:
    description = meta.get("content", "").strip()

# OG Image
og_image = ""

meta = (
    soup.find("meta", attrs={"property": "og:image"})
    or soup.find("meta", attrs={"name": "og:image"})
)

if meta:
    og_image = meta.get("content", "").strip()

print("Title:", title)
print("Slug:", slug)
print("Description:", description)
print("Image:", og_image)
print("URL:", page_url)

# Get Webflow Items
url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items"

response = requests.get(url, headers=HEADERS)
response.raise_for_status()

items = response.json().get("items", [])

existing = None

for item in items:
    field_data = item.get("fieldData", {})

    if field_data.get("slug") == slug:
        existing = item
        break

# Payload
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

# Update if exists
if existing:

    item_id = existing["id"]

    print(f"Updating item {item_id}")

    url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/{item_id}/live"

    response = requests.patch(
        url,
        headers=HEADERS,
        data=json.dumps(payload)
    )

# Otherwise create
else:

    print("Creating new CMS item")

    url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/live"

    response = requests.post(
        url,
        headers=HEADERS,
        data=json.dumps(payload)
    )

try:
    response.raise_for_status()

    print("=" * 60)
    print("✅ Webflow Sync Successful")
    print("=" * 60)

    print("Title :", title)
    print("Slug  :", slug)
    print("URL   :", page_url)

except requests.exceptions.HTTPError:

    print("=" * 60)
    print("❌ Webflow Error")
    print("=" * 60)

    print(response.status_code)
    print(response.text)

    raise
