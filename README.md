
# GitHub → Webflow CMS Sync

# Add in each HTML file before body
<script>
function updateHeight() {
  const height = Math.max(
    document.body.scrollHeight,
    document.documentElement.scrollHeight
  );

  window.parent.postMessage(
    {
      type: "SET_HEIGHT",
      height: height
    },
    "*"
  );
}

window.addEventListener("load", () => {
  updateHeight();

  setTimeout(updateHeight, 100);
  setTimeout(updateHeight, 500);
  setTimeout(updateHeight, 1000);
});

// Detect dynamic changes
new ResizeObserver(() => {
  updateHeight();
}).observe(document.body);

// Optional fallback
setInterval(updateHeight, 1000);
</script>

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
