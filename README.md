
# GitHub → Webflow CMS Sync

## Features

- Detect changed HTML files
- Extract metadata
- Create or update Webflow CMS items
- Publish automatically

## GitHub Secrets

WEBFLOW_TOKEN=xxxxxxxx

## Environment

Configured automatically by GitHub Actions.

## Push

```bash
git add .
git commit -m "New case study"
git push
```

The CMS item will automatically sync.
