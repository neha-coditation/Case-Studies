import os
import json
import requests
from bs4 import BeautifulSoup

WEBFLOW_TOKEN = os.environ.get("WEBFLOW_TOKEN")
COLLECTION_ID = os.environ.get("COLLECTION_ID")
GITHUB_PAGES = os.environ.get("GITHUB_PAGES")
HTML_FILE = os.environ.get("HTML_FILE")

if not HTML_FILE:
    print("⚠️ No HTML_FILE environment variable detected. Skipping sync.")
    exit(0)

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

# Title Fallback Extraction
title = ""
if soup.title:
    title = soup.title.text.strip()

if not title:
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)

if not title:
    title = slug.replace("-", " ").title()

# Description Extraction
description = ""
meta_desc = (
    soup.find("meta", attrs={"name": "description"})
    or soup.find("meta", attrs={"property": "og:description"})
)
if meta_desc:
    description = meta_desc.get("content", "").strip()

print("Parsed metadata:")
print(f"  Title:       {title}")
print(f"  Slug:        {slug}")
print(f"  Description: {description}")
print(f"  URL:         {page_url}")

# Fetch Webflow Items to check for existing slug
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

# Payload Structure
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

# Update or Create
try:
    if existing:
        item_id = existing["id"]
        print(f"\n🔄 Updating existing item: {item_id}")
        url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/{item_id}/live"
        response = requests.patch(
            url,
            headers=HEADERS,
            data=json.dumps(payload)
        )
    else:
        print("\n✨ Creating new CMS item")
        url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/live"
        response = requests.post(
            url,
            headers=HEADERS,
            data=json.dumps(payload)
        )

    response.raise_for_status()
    
    print("=" * 60)
    print("✅ Webflow Sync Successful")
    print("=" * 60)

except requests.exceptions.HTTPError as err:
    print("=" * 60)
    print("❌ Webflow API Error Detailed Output:")
    print("=" * 60)
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)
    raise err
